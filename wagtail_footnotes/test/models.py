from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import InlinePanel, RichTextFieldPanel

class InformationPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        RichTextFieldPanel("body"),
        InlinePanel("footnotes", label="Footnotes"),
    ]
