from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField

from .fields import CustomUUIDField
from .widgets import ReadonlyUUIDInput


class Footnote(models.Model):
    """
    Footnote has a UUID field which is set using JavaScript on object creation
    so that it is available immediately for hardcoding a reference to the
    footnote in the rich text of the page.
    """

    page = ParentalKey("wagtailcore.Page", related_name="footnotes")
    uuid = CustomUUIDField(
        unique=True,
        verbose_name="ID",
        help_text="The ID of the footnote is shown in the rich text editor for "
        "reference.",
    )
    text = RichTextField(features=["bold", "italic", "link"])

    panels = [FieldPanel("text"), FieldPanel("uuid", widget=ReadonlyUUIDInput)]
