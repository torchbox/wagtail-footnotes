from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey

try:
    from wagtail.admin.panels import FieldPanel, InlinePanel
except ImportError:
    # Wagtail<3.0
    from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

try:
    from wagtail.fields import RichTextField
except ImportError:
    # Wagtail<3.0
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
        verbose_name="ID",
        help_text="The ID of the footnote is shown in the rich text editor for "
        "reference.",
    )
    text = RichTextField(
        features=getattr(
            settings, "WAGTAIL_FOOTNOTES_TEXT_FEATURES", ["bold", "italic", "link"]
        )
    )

    panels = [FieldPanel("text"), FieldPanel("uuid", widget=ReadonlyUUIDInput)]

    class Meta:
        unique_together = ("page", "uuid")
