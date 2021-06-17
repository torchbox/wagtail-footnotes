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
    def test_factory(self):
        rich_text = RichText("test")
        page = factories.TestPage(body__0__paragraph__value=rich_text)
        self.assertEqual(str(page.body[0]), str(rich_text))

    def test_factory_with_empty_body(self):
        factories.TestPage(body={})
