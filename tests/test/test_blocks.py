import json
import uuid as uuid_module

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

        uuid_a = str(uuid_module.uuid4())
        uuid_b = str(uuid_module.uuid4())
        self.test_page_counter_isolation = TestPageStreamField(
            title="Test Page Counter Isolation",
            slug="test-page-counter-isolation",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": (
                            f'<p>A first <footnote id="{uuid_a}">[{uuid_a[:6]}]</footnote></p>'
                            f'<p>A second <footnote id="{uuid_a}">[{uuid_a[:6]}]</footnote></p>'
                            f'<p>B once <footnote id="{uuid_b}">[{uuid_b[:6]}]</footnote></p>'
                        ),
                    }
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_counter_isolation)
        self.test_page_counter_isolation.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_counter_isolation,
            uuid=uuid_a,
            text="Footnote A",
        )
        Footnote.objects.create(
            page=self.test_page_counter_isolation,
            uuid=uuid_b,
            text="Footnote B",
        )

        uuid_cross = str(uuid_module.uuid4())
        self.test_page_cross_block_refs = TestPageStreamField(
            title="Test Page Cross Block Refs",
            slug="test-page-cross-block-refs",
            body=json.dumps(
                [
                    {
                        "type": "paragraph",
                        "value": f'<p>Block 1 <footnote id="{uuid_cross}">[{uuid_cross[:6]}]</footnote></p>',
                    },
                    {
                        "type": "paragraph",
                        "value": f'<p>Block 2 <footnote id="{uuid_cross}">[{uuid_cross[:6]}]</footnote></p>',
                    },
                ]
            ),
        )
        home_page.add_child(instance=self.test_page_cross_block_refs)
        self.test_page_cross_block_refs.save_revision().publish()
        Footnote.objects.create(
            page=self.test_page_cross_block_refs,
            uuid=uuid_cross,
            text="Cross-block footnote",
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

    def test_block_reference_counters_are_isolated_per_footnote(self):
        """Reference counter for footnote B starts at 1 and does not bleed from footnote A's count."""
        body = self.test_page_counter_isolation.body
        rtb = body.stream_block.child_blocks["paragraph"]
        value = rtb.get_prep_value(body[0].value)
        context = self.test_page_counter_isolation.get_context(self.client.get("/"))
        out = rtb.render(value, context=context)
        # Footnote A is referenced twice (1-1, 1-2); footnote B's counter resets to 1 (2-1), not 3
        self.assertHTMLEqual(
            out,
            '<p>A first <a href="#footnote-1" id="footnote-source-1-1"><sup>[1]</sup></a></p>'
            '<p>A second <a href="#footnote-1" id="footnote-source-1-2"><sup>[1]</sup></a></p>'
            '<p>B once <a href="#footnote-2" id="footnote-source-2-1"><sup>[2]</sup></a></p>',
        )

    def test_same_footnote_across_multiple_block_renders(self):
        """footnotes_list persists across block renders so a second-block reference correctly increments."""
        body = self.test_page_cross_block_refs.body
        context = self.test_page_cross_block_refs.get_context(self.client.get("/"))
        rtb = body.stream_block.child_blocks["paragraph"]

        # Render each block in sequence using the same context so footnotes_list accumulates
        out_block1 = rtb.render(rtb.get_prep_value(body[0].value), context=context)
        out_block2 = rtb.render(rtb.get_prep_value(body[1].value), context=context)

        # First block gets reference index 1, second block gets reference index 2
        self.assertHTMLEqual(
            out_block1,
            '<p>Block 1 <a href="#footnote-1" id="footnote-source-1-1"><sup>[1]</sup></a></p>',
        )
        self.assertHTMLEqual(
            out_block2,
            '<p>Block 2 <a href="#footnote-1" id="footnote-source-1-2"><sup>[1]</sup></a></p>',
        )
