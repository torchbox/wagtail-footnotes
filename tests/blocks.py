from wagtail import blocks

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class CustomBlock(blocks.StreamBlock):
    paragraph = RichTextBlockWithFootnotes(features=["footnotes"])
