import json

from bs4 import BeautifulSoup as bs4
from django.test import override_settings
from django.urls import reverse
from django.utils import translation
from wagtail.models import Locale, Page
from wagtail.test.utils import TestCase, WagtailTestUtils

from wagtail_footnotes.models import Footnote

from ..models import TestPageStreamField


@override_settings(
    LANGUAGES=[
        ("en", "English"),
        ("fr", "French"),
        ("de", "German"),
    ],
    WAGTAIL_CONTENT_LANGUAGES=[
        ("en", "English"),
        ("fr", "French"),
        ("de", "German"),
    ],
)
class TestSubmitPageTranslationView(WagtailTestUtils, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.en_locale = Locale.objects.first()
        cls.fr_locale = Locale.objects.create(language_code="fr")
        cls.de_locale = Locale.objects.create(language_code="de")

        cls.en_homepage = Page.objects.get(title="Welcome to your new Wagtail site!")
        cls.fr_homepage = cls.en_homepage.copy_for_translation(cls.fr_locale)
        cls.fr_homepage.save_revision().publish()
        cls.de_homepage = cls.en_homepage.copy_for_translation(cls.de_locale)
        cls.de_homepage.save_revision().publish()

        cls.uuid = "f291a4b7-5ac5-4030-b341-b1993efb2ad2"
        cls.en_test_page = TestPageStreamField(
            title="Test Page With Footnote",
            slug="test-page-with-footnote",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": f'<p>This is a paragraph with a footnote. <footnote id="{cls.uuid}">1</footnote></p>',
                    },
                ]
            ),
        )
        cls.en_homepage.add_child(instance=cls.en_test_page)
        cls.en_test_page.save_revision().publish()
        cls.en_footnote = Footnote.objects.create(
            page=cls.en_test_page,
            uuid=cls.uuid,
            text="This is a footnote",
        )
        cls.url = reverse(
            "simple_translation:submit_page_translation", args=(cls.en_test_page.id,)
        )

    def setUp(self):
        super().setUp()
        self.login()

    def test_translating_page_translates_footnote(self):
        de = self.de_locale.id
        fr = self.fr_locale.id
        data = {"locales": [de, fr], "include_subtree": True}
        self.client.post(self.url, data, follow=True)

        de_footnote = self.en_footnote.get_translation(de)
        self.assertEqual(de_footnote.text, self.en_footnote.text)
        self.assertEqual(de_footnote.uuid, self.en_footnote.uuid)
        de_test_page = self.en_test_page.get_translation(de)
        self.assertCountEqual(de_test_page.footnotes.all(), [de_footnote])

        fr_footnote = self.en_footnote.get_translation(fr)
        self.assertEqual(fr_footnote.text, self.en_footnote.text)
        self.assertEqual(fr_footnote.uuid, self.en_footnote.uuid)
        fr_test_page = self.en_test_page.get_translation(fr)
        self.assertCountEqual(fr_test_page.footnotes.all(), [fr_footnote])

        # Can also change the text:
        fr_footnote.text = "This is a French translated footnote"
        fr_footnote.save(update_fields=["text"])
        fr_footnote.refresh_from_db()
        en_footnote = self.en_footnote
        en_footnote.refresh_from_db()
        self.assertEqual(fr_footnote.text, "This is a French translated footnote")
        self.assertNotEqual(fr_footnote.text, en_footnote.text)

    def test_translated_page_shows_translated_footnote(self):
        fr = self.fr_locale.id
        data = {"locales": [fr], "include_subtree": True}
        response = self.client.post(self.url, data, follow=True)

        fr_test_page = self.en_test_page.get_translation(fr)

        self.assertRedirects(
            response, reverse("wagtailadmin_pages:edit", args=[fr_test_page.pk])
        )

        self.assertIn(
            "The page 'Test Page With Footnote' was successfully created in French",
            [msg.message for msg in response.context["messages"]],
        )

        fr_footnote = self.en_footnote.get_translation(fr)
        self.assertEqual(fr_footnote.text, self.en_footnote.text)
        self.assertEqual(fr_footnote.uuid, self.en_footnote.uuid)
        self.assertCountEqual(fr_test_page.footnotes.all(), [fr_footnote])

        fr_test_page.title = ("[FR] Test Page With Footnote",)
        fr_test_page.body = json.dumps(
            [
                {
                    "type": "paragraph",
                    "value": f'<p>This is a French paragraph with a footnote. <footnote id="{self.uuid}">1</footnote></p>',
                },
            ]
        )
        fr_test_page.save_revision().publish()
        fr_test_page.refresh_from_db()

        # Can also change the text:
        fr_footnote.text = "This is a French translated footnote"
        fr_footnote.save()

        translation.activate("fr")

        response = self.client.get(fr_test_page.get_full_url())
        self.assertEqual(response.status_code, 200)

        soup = bs4(response.content, "html.parser")

        # Test that required html tags are present with correct
        # attrs that enable the footnotes to respond to clicks
        source_anchor = soup.find("a", {"id": "footnote-source-1"})
        self.assertTrue(source_anchor)

        source_anchor_string = str(source_anchor)
        self.assertIn("<sup>[1]</sup>", source_anchor_string)
        self.assertIn('href="#footnote-1"', source_anchor_string)
        self.assertIn('id="footnote-source-1"', source_anchor_string)

        footnotes = soup.find("div", {"class": "footnotes"})
        self.assertTrue(footnotes)

        footnotes_string = str(footnotes)
        self.assertIn('id="footnote-1"', footnotes_string)
        self.assertIn('href="#footnote-source-1"', footnotes_string)
        self.assertIn("[1] This is a French translated footnote", footnotes_string)
