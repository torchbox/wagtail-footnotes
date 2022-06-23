import re

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

try:
    from wagtail.blocks import RichTextBlock
except ImportError:
    # Wagtail<3.0
    from wagtail.core.blocks import RichTextBlock

try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page


FIND_FOOTNOTE_TAG = re.compile(r'<footnote id="(.*?)">.*?</footnote>')


class RichTextBlockWithFootnotes(RichTextBlock):
    """
    Rich Text block that renders footnotes in the format
    '<footnote id="long-id">short-id</footnote>' as anchor elements. It also
    adds the Footnote object to the 'page' object for later use. It uses
    'page' because variables added to 'context' do not persist into the
    final template context.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.features:
            self.features = []
        if "footnotes" not in self.features:
            self.features.append("footnotes")

    def replace_footnote_tags(self, value, html, context=None):
        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        if not isinstance(new_context.get("page"), Page):
            return html

        page = new_context["page"]
        if not hasattr(page, "footnotes_list"):
            page.footnotes_list = []
        self.footnotes = {str(footnote.uuid): footnote for footnote in page.footnotes.all()}

        def replace_tag(match):
            try:
                index = self.process_footnote(match.group(1), page)
            except (KeyError, ValidationError):
                return ""
            else:
                return f'<a href="#footnote-{index}" id="footnote-source-{index}"><sup>[{index}]</sup></a>'

        return mark_safe(FIND_FOOTNOTE_TAG.sub(replace_tag, html))

    def render(self, value, context=None):
        if not self.get_template(context=context):
            return self.render_basic(value, context=context)

        html = super().render(value, context=context)
        return self.replace_footnote_tags(value, html, context=context)

    def render_basic(self, value, context=None):
        html = super().render_basic(value, context)

        return self.replace_footnote_tags(value, html, context=context)

    def process_footnote(self, footnote_id, page):
        footnote = self.footnotes[footnote_id]
        if footnote not in page.footnotes_list:
            page.footnotes_list.append(footnote)
        # Add 1 to the index as footnotes are indexed starting at 1 not 0.
        return page.footnotes_list.index(footnote) + 1
