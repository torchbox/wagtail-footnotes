from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
else:
    from wagtail.core import blocks

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class CustomBlock(blocks.StreamBlock):
    paragraph = RichTextBlockWithFootnotes(features=["footnotes"])
