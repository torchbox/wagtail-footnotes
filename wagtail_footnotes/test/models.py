from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.admin.panels import FieldPanel, InlinePanel
    from wagtail.fields import RichTextField, StreamField
    from wagtail.models import Page
else:    
    from wagtail.admin.edit_handlers import InlinePanel, RichTextFieldPanel
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.core.models import Page

from wagtail_footnotes.test.blocks import CustomBlock


class TestPageStreamField(Page):
    template = "test/test_page_stream_field.html"

    body = StreamField(CustomBlock(), use_json_field=True) if WAGTAIL_VERSION >= (3, 0) else StreamField(CustomBlock())
    
    content_panels = Page.content_panels + [
        FieldPanel("body") if WAGTAIL_VERSION >= (3, 0) else RichTextFieldPanel("body"),
        InlinePanel("footnotes", label="Footnotes"),
    ]
