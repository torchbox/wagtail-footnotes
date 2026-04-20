import json
import uuid as uuid_module

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
            username="admin",
            email="",
            password="password",  # noqa: S106
        )

        uuid_multi = str(uuid_module.uuid4())
        self.test_page_multi_refs = TestPageStreamField(
            title="Test Page Multi Refs",
            slug="test-page-multi-refs",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": (
                            f'<p>First reference <footnote id="{uuid_multi}">1</footnote>'
                            f' and second reference <footnote id="{uuid_multi}">1</footnote></p>'
                        ),
                    }
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_multi_refs)
        self.test_page_multi_refs.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_multi_refs,
            uuid=uuid_multi,
            text="Shared footnote",
        )

        uuid_a = str(uuid_module.uuid4())
        uuid_b = str(uuid_module.uuid4())
        self.test_page_two_footnotes = TestPageStreamField(
            title="Test Page Two Footnotes",
            slug="test-page-two-footnotes",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": (
                            f'<p>Footnote A <footnote id="{uuid_a}">1</footnote>'
                            f' and footnote B <footnote id="{uuid_b}">2</footnote></p>'
                        ),
                    }
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_two_footnotes)
        self.test_page_two_footnotes.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_two_footnotes,
            uuid=uuid_a,
            text="Footnote A text",
        )
        Footnote.objects.create(
            page=self.test_page_two_footnotes,
            uuid=uuid_b,
            text="Footnote B text",
        )

        uuid_cross = str(uuid_module.uuid4())
        self.test_page_cross_blocks = TestPageStreamField(
            title="Test Page Cross Blocks",
            slug="test-page-cross-blocks",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": f'<p>Block 1 reference <footnote id="{uuid_cross}">1</footnote></p>',
                    },
                    {
                        "type": "paragraph",
                        "value": f'<p>Block 2 reference <footnote id="{uuid_cross}">1</footnote></p>',
                    },
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_cross_blocks)
        self.test_page_cross_blocks.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_cross_blocks,
            uuid=uuid_cross,
            text="Cross-block footnote",
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
        source_anchor = soup.find("a", {"id": "footnote-source-1-1"})
        self.assertTrue(source_anchor)

        source_anchor_string = str(source_anchor)
        self.assertIn("<sup>[1]</sup>", source_anchor_string)
        self.assertIn('href="#footnote-1"', source_anchor_string)
        self.assertIn('id="footnote-source-1-1"', source_anchor_string)

        footnotes = soup.find("div", {"class": "footnotes"})
        self.assertTrue(footnotes)

        footnotes_string = str(footnotes)
        self.assertIn('id="footnote-1"', footnotes_string)
        self.assertIn('href="#footnote-source-1-1"', footnotes_string)
        self.assertIn("This is a footnote", footnotes_string)

    def test_multiple_references_to_same_footnote_back_links(self):
        """footnotes.html renders individual back-links for each in-text reference."""
        response = self.client.get("/test-page-multi-refs/")
        self.assertEqual(response.status_code, 200)
        soup = bs4(response.content, "html.parser")

        # Both in-text source anchors are present
        self.assertTrue(soup.find("a", {"id": "footnote-source-1-1"}))
        self.assertTrue(soup.find("a", {"id": "footnote-source-1-2"}))

        # The footnote list contains back-links pointing to each source anchor
        footnotes_string = str(soup.find("div", {"class": "footnotes"}))
        self.assertIn('href="#footnote-source-1-1"', footnotes_string)
        self.assertIn('href="#footnote-source-1-2"', footnotes_string)
        self.assertIn("Shared footnote", footnotes_string)

    def test_two_footnotes_each_referenced_once(self):
        """Two distinct footnotes each get unique IDs and appear in text order."""
        response = self.client.get("/test-page-two-footnotes/")
        self.assertEqual(response.status_code, 200)
        soup = bs4(response.content, "html.parser")

        # Each footnote's in-text anchor uses its position in footnotes_list as the first index
        self.assertTrue(soup.find("a", {"id": "footnote-source-1-1"}))
        self.assertTrue(soup.find("a", {"id": "footnote-source-2-1"}))

        # Both footnotes appear in the list in text order with correct back-links
        footnotes_string = str(soup.find("div", {"class": "footnotes"}))
        self.assertIn('id="footnote-1"', footnotes_string)
        self.assertIn('id="footnote-2"', footnotes_string)
        self.assertIn('href="#footnote-source-1-1"', footnotes_string)
        self.assertIn('href="#footnote-source-2-1"', footnotes_string)
        self.assertIn("Footnote A text", footnotes_string)
        self.assertIn("Footnote B text", footnotes_string)

    def test_same_footnote_referenced_across_multiple_blocks(self):
        """A footnote referenced in two separate blocks accumulates back-links correctly."""
        response = self.client.get("/test-page-cross-blocks/")
        self.assertEqual(response.status_code, 200)
        soup = bs4(response.content, "html.parser")

        # footnotes_list persists across block renders, so each block's reference gets a unique anchor
        self.assertTrue(soup.find("a", {"id": "footnote-source-1-1"}))
        self.assertTrue(soup.find("a", {"id": "footnote-source-1-2"}))

        # The footnote list back-links cover both in-text occurrences
        footnotes_string = str(soup.find("div", {"class": "footnotes"}))
        self.assertIn('href="#footnote-source-1-1"', footnotes_string)
        self.assertIn('href="#footnote-source-1-2"', footnotes_string)
        self.assertIn("Cross-block footnote", footnotes_string)

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
