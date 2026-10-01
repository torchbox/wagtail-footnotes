from wagtail import blocks

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class CaptionRichTextFilterBlock(blocks.StructBlock):
    """Renders its caption with the |richtext filter."""

    caption = RichTextBlockWithFootnotes(features=["footnotes"])

    class Meta:
        template = "test/blocks/caption_richtext_filter.html"


class CaptionIncludeBlock(blocks.StructBlock):
    """Renders its caption with {% include_block value.caption %}."""

    caption = RichTextBlockWithFootnotes(features=["footnotes"])

    class Meta:
        template = "test/blocks/caption_include_block.html"


class CustomBlock(blocks.StreamBlock):
    paragraph = RichTextBlockWithFootnotes(features=["footnotes"])
    caption_richtext_filter = CaptionRichTextFilterBlock()
    caption_include_block = CaptionIncludeBlock()
