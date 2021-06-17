from wagtail.admin.edit_handlers import InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from . import blocks


class TestPage(Page):
    # template = "patterns/pages/home/home_page.html"

    body = StreamField(blocks.CustomBlock())

    content_panels = [
        StreamFieldPanel("body"),
        InlinePanel("footnotes", label="Footnotes"),
    ]
