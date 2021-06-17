import wagtail_factories

from django.test import TestCase

from wagtail.core.rich_text import RichText

from .. import factories


class TestRichTextBlockWithFootnotesFactory(TestCase):
    def test_factory(self):
        rich_text = RichText("test")
        value = factories.RichTextBlockWithFootnotes(value=rich_text)
        self.assertEqual(str(value), str(rich_text))


class TestCustomBlockFactory(TestCase):
    def test_factory(self):
        rich_text = RichText("test")
        value = factories.CustomBlock(paragraph__value=rich_text)
        self.assertEqual(str(value["paragraph"]), str(rich_text))


class TestPageFactory(TestCase):
    def setUp(self):
        # Build home page and default site
        self.root_page = wagtail_factories.PageFactory(parent=None)
        self.site = wagtail_factories.SiteFactory(
            is_default_site=True, root_page=self.root_page
        )

    def test_factory(self):
        # Build page
        rich_text = RichText("test")
        page = factories.TestPage(
            parent=self.root_page,
            body__0__paragraph__value=rich_text,
        )
        # Test body value
        self.assertEqual(str(page.body[0]), str(rich_text))
        # Test page render
        response = self.client.get(page.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, page.title)
        self.assertContains(response, str(rich_text))

    def test_factory_with_empty_body(self):
        # Build page
        page = factories.TestPage(parent=self.root_page, body={})
        # Test page render
        response = self.client.get(page.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, page.title)
