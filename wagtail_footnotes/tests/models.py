from django.db import models
from wagtail.admin.edit_handlers import InlinePanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtail_footnotes.blocks import RichTextBlockWithFootnotes


class CustomBlock(blocks.StreamBlock):
    paragraph = RichTextBlockWithFootnotes(features=["footnotes"])

    # class Meta:
    #     template = "patterns/molecules/streamfield/stream_block.html"


class TestPage(Page):
    # template = "patterns/pages/home/home_page.html"

    body = StreamField(CustomBlock())

    content_panels = [
        StreamFieldPanel("body"),
        InlinePanel("footnotes", label="Footnotes"),
    ]
