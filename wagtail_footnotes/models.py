from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin

from wagtail_footnotes.fields import CustomUUIDField
from wagtail_footnotes.widgets import ReadonlyUUIDInput


class Footnote(TranslatableMixin, models.Model):
    """
    Footnote has a UUID field which is set using JavaScript on object creation
    so that it is available immediately for hardcoding a reference to the
    footnote in the rich text of the page.
    """

    page = ParentalKey("wagtailcore.Page", related_name="footnotes")
    uuid = CustomUUIDField(
        verbose_name="ID",
        help_text=_(
            "The ID of the footnote is shown in the rich text editor for " "reference."
        ),
    )
    text = RichTextField(
        features=getattr(
            settings, "WAGTAIL_FOOTNOTES_TEXT_FEATURES", ["bold", "italic", "link"]
        )
    )

    panels = [FieldPanel("text"), FieldPanel("uuid", widget=ReadonlyUUIDInput)]

    class Meta(TranslatableMixin.Meta):
        unique_together = [("page", "uuid"), ("translation_key", "locale")]

    def __str__(self):
        return str(self.uuid)
