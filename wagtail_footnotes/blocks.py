import re

from django.conf import settings
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from wagtail.blocks import RichTextBlock
from wagtail.models import Page

from wagtail_footnotes.models import Footnote


FIND_FOOTNOTE_TAG = re.compile(r'<footnote id="(.*?)">.*?</footnote>')


class RichTextBlockWithFootnotes(RichTextBlock):
    """
    Rich Text block that renders footnotes in the format
    '<footnote id="long-id">short-id</footnote>' as anchor elements. It also
    adds the Footnote object(s) to the 'page' object for later use. It uses
    'page' because variables added to 'context' do not persist into the
    final template context.
    """

    all_footnotes: dict[str, Footnote]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.features:
            self.features = []
        if "footnotes" not in self.features:
            self.features.append("footnotes")

    def render_footnote_tag(self, index: int, reference_index: int):
        template_name = getattr(
            settings,
            "WAGTAIL_FOOTNOTES_REFERENCE_TEMPLATE",
            "wagtail_footnotes/includes/footnote_reference.html",
        )
        template = get_template(template_name)
        return template.render({"index": index, "reference_index": reference_index})

    def replace_footnote_tags(self, value, html, context=None):
        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        page = new_context.get("page")
        if page is None or not isinstance(page, Page):
            return html

        # Map Footnote UUIDs to Footnote instances to simplify lookups once a reference has been found in the text.
        # NOTE: Footnotes may exist in the database for a given page but this does not necessarily mean that the
        # footnote was referenced in the text.
        self.all_footnotes = {
            str(footnote.uuid): footnote for footnote in page.footnotes.all()
        }

        # Patch the page to track the footnotes that are actually referenced in the text, so that they can be rendered
        # in footnotes.html
        if not hasattr(page, "footnotes_list"):
            page.footnotes_list = []

        def replace_tag(match):
            footnote_uuid = match.group(1)
            try:
                footnote = self.attach_footnote_to_page(footnote_uuid, page)
            except KeyError:
                return ""
            else:
                # Add 1 to the footnote index as footnotes are rendered in footnotes.html using `{{ forloop.counter }}`
                # which is 1-based.
                footnote_index = page.footnotes_list.index(footnote) + 1
                reference_index = footnote.references[-1]
                # Supplying both indexes allows for unique id values to be generated in the HTML. E.g., the first
                # reference to the first footnote will have `id="footnote-source-1-1"`, and the second reference to the
                # first footnote will have `id="footnote-source-1-2"`, etc.
                return self.render_footnote_tag(footnote_index, reference_index)

        # note: we return safe html
        return mark_safe(FIND_FOOTNOTE_TAG.sub(replace_tag, html))  # noqa: S308

    def render(self, value, context=None):
        html = super().render(value, context=context)
        return self.replace_footnote_tags(value, html, context=context)

    def attach_footnote_to_page(self, footnote_uuid: str, page: Page) -> Footnote:
        """Finds the Footnote object matching `footnote_uuid`, then modifies it to track how many times it has been
        referenced, and attaches it to the `page` so the footnote can be rendered in the page template.
        """
        # Fetch the unmodified Footnote
        footnote = self.all_footnotes[footnote_uuid]

        # If this is the first time the Footnote has been referenced, modify it to track references before appending it
        # to the page
        if footnote not in page.footnotes_list:
            footnote.references = [1]
            page.footnotes_list.append(footnote)
        else:
            # If this Footnote has been processed by a previous reference, fetch the modified Footnote from the page and
            # update its reference tracking
            footnote_index = page.footnotes_list.index(footnote)
            footnote = page.footnotes_list[footnote_index]
            # Update the references e.g., [1, 2]
            footnote.references.append(footnote.references[-1] + 1)
            # Update the page with the updated footnote
            page.footnotes_list[footnote_index] = footnote
        return footnote
