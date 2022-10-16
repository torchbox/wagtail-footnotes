from django.test import TestCase
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
    from wagtail.fields import StreamBlock
else:
    from wagtail.core import blocks
    from wagtail.core.fields import StreamBlock


class TestBlocks(TestCase):
    def test_custom_block(self):
        block = StreamBlock([
            ("paragraph", RichTextBlockWithFootnotes(features=["footnotes"])),
        ])
        rich_text_block_with_footnotes = block.child_blocks["paragraph"]
        self.assertIsInstance(rich_text_block_with_footnotes, blocks.RichTextBlock)
        self.assertEqual(rich_text_block_with_footnotes.features, ["footnotes"])
        
