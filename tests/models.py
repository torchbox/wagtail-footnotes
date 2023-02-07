from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import CustomBlock


class TestPageStreamField(Page):
    template = "test/test_page_stream_field.html"

    body = StreamField(CustomBlock(), use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        InlinePanel("footnotes", label="Footnotes"),
    ]
