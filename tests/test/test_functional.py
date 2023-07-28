import json

from bs4 import BeautifulSoup as bs4
from django.contrib.auth.models import User
from django.test import TestCase
from wagtail.models import Page

from wagtail_footnotes.models import Footnote

from ..models import TestPageStreamField


class TestFunctional(TestCase):
    def setUp(self):
        home_page = Page.objects.get(title="Welcome to your new Wagtail site!")

        self.test_page_no_footnote = TestPageStreamField(
            title="Test Page No Footnote",
            slug="test-page-no-footnote",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": "<p>This is a paragraph with no footnote.</p>",
                    }
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_no_footnote)
        self.test_page_no_footnote.save_revision().publish()

        uuid = "f291a4b7-5ac5-4030-b341-b1993efb2ad2"
        self.test_page_with_footnote = TestPageStreamField(
            title="Test Page With Footnote",
            slug="test-page-with-footnote",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": f'<p>This is a paragraph with a footnote. <footnote id="{uuid}">1</footnote></p>',
                    },
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_with_footnote)
        self.test_page_with_footnote.save_revision().publish()
        self.footnote = Footnote.objects.create(
            page=self.test_page_with_footnote,
            uuid=uuid,
            text="This is a footnote",
        )

        self.admin_user = User.objects.create_superuser(
            username="admin", email="", password="password"  # noqa: S106
        )

    def test_no_footnote(self):
        response = self.client.get("/test-page-no-footnote/")
        self.assertEqual(response.status_code, 200)

        soup = bs4(response.content, "html.parser")

        # test that these html tags are not present
        self.assertEqual(soup.find("sup"), None)
        self.assertEqual(soup.find("a"), None)
        self.assertEqual(soup.find("div", {"class": "footnotes"}), None)
        self.assertEqual(soup.find("ol"), None)
        self.assertEqual(soup.find("li"), None)
        self.assertEqual(soup.find("p").text, "This is a paragraph with no footnote.")

    def test_with_footnote(self):
        response = self.client.get("/test-page-with-footnote/")
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
        self.assertIn("[1] This is a footnote", footnotes_string)

    def test_edit_page_with_footnote(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            f"/admin/pages/{self.test_page_with_footnote.id}/edit/"
        )

        data_block = (
            response.context["form"]
            .fields["body"]
            .get_bound_field(response.context["form"], "body")
        )
        soup = bs4(str(data_block), "html.parser")

        # Test that the footnote uuid is present in the html
        self.assertIn(self.footnote.uuid, str(soup))
