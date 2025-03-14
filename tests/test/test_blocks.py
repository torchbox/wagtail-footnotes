import json

from django.test import TestCase, override_settings
from wagtail import blocks
from wagtail.fields import StreamBlock
from wagtail.models import Page

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes
from wagtail_footnotes.models import Footnote

from ..models import TestPageStreamField


class TestBlocks(TestCase):
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
                        "value": (
                            f'<p>This is a paragraph with a footnote. <footnote id="{uuid}">[{uuid[:6]}]</footnote></p>'
                        ),
                    },
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_with_footnote)
        self.test_page_with_footnote.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_with_footnote,
            uuid=uuid,
            text="This is a footnote",
        )

        self.test_page_with_multiple_references_to_the_same_footnote = TestPageStreamField(
            title="Test Page With Multiple References to the Same Footnote",
            slug="test-page-with-multiple-references-to-the-same-footnote",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": (
                            f'<p>This is a paragraph with a footnote. <footnote id="{uuid}">[{uuid[:6]}]</footnote></p>'
                            f"<p>This is another paragraph with a reference to the same footnote. "
                            f'<footnote id="{uuid}">[{uuid[:6]}]</footnote></p>'
                        ),
                    },
                ]
            ),
        )
        home_page.add_child(
            instance=self.test_page_with_multiple_references_to_the_same_footnote
        )
        self.test_page_with_multiple_references_to_the_same_footnote.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_with_multiple_references_to_the_same_footnote,
            uuid=uuid,
            text="This is a footnote",
        )

    def test_block_with_no_features(self):
        block = RichTextBlockWithFootnotes()
        self.assertIsInstance(block, blocks.RichTextBlock)
        self.assertEqual(block.features, ["footnotes"])

    def test_block_with_features(self):
        block = RichTextBlockWithFootnotes(features=["h1", "h2"])
        self.assertIsInstance(block, blocks.RichTextBlock)
        self.assertEqual(block.features, ["h1", "h2", "footnotes"])

    def test_block_with_stream_block(self):
        block = StreamBlock([("rich_text", RichTextBlockWithFootnotes())])
        self.assertIsInstance(block, StreamBlock)
        self.assertEqual(block.child_blocks["rich_text"].features, ["footnotes"])

    def test_block_with_stream_block_with_features(self):
        block = StreamBlock(
            [("rich_text", RichTextBlockWithFootnotes(features=["h1", "h2"]))]
        )
        self.assertIsInstance(block, StreamBlock)
        self.assertEqual(
            block.child_blocks["rich_text"].features, ["h1", "h2", "footnotes"]
        )

    def test_block_with_struct_block(self):
        class StructBlock(blocks.StructBlock):
            rich_text = RichTextBlockWithFootnotes()

        block = StructBlock()
        self.assertIsInstance(block, blocks.StructBlock)
        self.assertEqual(block.child_blocks["rich_text"].features, ["footnotes"])

    def test_block_with_struct_block_with_features(self):
        class StructBlock(blocks.StructBlock):
            rich_text = RichTextBlockWithFootnotes(features=["h1", "h2"])

        block = StructBlock()
        self.assertIsInstance(block, blocks.StructBlock)
        self.assertEqual(
            block.child_blocks["rich_text"].features, ["h1", "h2", "footnotes"]
        )

    def test_block_replace_footnote_tags(self):
        block = RichTextBlockWithFootnotes()
        html = block.replace_footnote_tags(None, "foo")
        self.assertEqual(html, "foo")

    def test_block_replace_footnote_render(self):
        rtb = self.test_page_with_footnote.body.stream_block.child_blocks["paragraph"]
        value = rtb.get_prep_value(self.test_page_with_footnote.body[0].value)
        context = self.test_page_with_footnote.get_context(self.client.get("/"))
        out = rtb.render(value, context=context)
        result = (
            '<p>This is a paragraph with a footnote. <a href="#footnote-1" id="footnote-source-1-1"><sup>[1]</sup></a>'
            "</p>"
        )
        self.assertHTMLEqual(out, result)

    def test_block_replace_footnote_with_multiple_references_render(self):
        body = self.test_page_with_multiple_references_to_the_same_footnote.body
        rtb = body.stream_block.child_blocks["paragraph"]
        value = rtb.get_prep_value(body[0].value)
        context = (
            self.test_page_with_multiple_references_to_the_same_footnote.get_context(
                self.client.get("/")
            )
        )
        out = rtb.render(value, context=context)
        result = (
            '<p>This is a paragraph with a footnote. <a href="#footnote-1" id="footnote-source-1-1"><sup>[1]</sup></a>'
            '</p><p>This is another paragraph with a reference to the same footnote. <a href="#footnote-1" '
            'id="footnote-source-1-2"><sup>[1]</sup></a></p>'
        )
        self.assertHTMLEqual(out, result)

    def test_render_footnote_tag(self):
        block = RichTextBlockWithFootnotes()
        html = block.render_footnote_tag(index=2, reference_index=1)
        self.assertHTMLEqual(
            html, '<a href="#footnote-2" id="footnote-source-2-1"><sup>[2]</sup></a>'
        )

    @override_settings(
        WAGTAIL_FOOTNOTES_REFERENCE_TEMPLATE="test/endnote_reference.html"
    )
    def test_render_footnote_tag_new_template(self):
        block = RichTextBlockWithFootnotes()
        html = block.render_footnote_tag(index=2, reference_index=1)
        self.assertHTMLEqual(
            html, '<a href="#endnote-2" id="endnote-source-2-1"><sup>2</sup></a>'
        )
