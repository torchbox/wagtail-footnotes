from wagtail.core import blocks

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class CustomBlock(blocks.StreamBlock):
    paragraph = RichTextBlockWithFootnotes(features=["footnotes"])

    # class Meta:
    #     template = "patterns/molecules/streamfield/stream_block.html"
