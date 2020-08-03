import re

from django.core.exceptions import ValidationError
from wagtail.core.blocks import RichTextBlock

FIND_FOOTNOTE_TAG = re.compile(r'<footnote id="(.*?)">.*?</footnote>')


class RichTextBlockWithFootnotes(RichTextBlock):
    """
    Rich Text block that renders footnotes in the format
    '<footnote id="long-id">short-id</footnote>' as anchor elements. It also
    adds the Footnote object to the 'request' object for later use. It uses
    'request' because variables added to 'context' do not persist into the
    final template context.
    """

    def render_basic(self, value, context=None):
        html = super().render_basic(value, context)

        def replace_tag(match):
            try:
                index = self.process_footnote(match.group(1), context)
            except (KeyError, ValidationError):
                return ""
            else:
                return f'<a href="#footnote-{index}" id="footnote-source-{index}"><sup>[{index}]</sup></a>'

        return FIND_FOOTNOTE_TAG.sub(replace_tag, html)

    def process_footnote(self, footnote_id, context):
        footnotes = self.get_footnotes(context["page"])
        footnote = context["page"].footnotes.get(uuid=footnote_id)
        if footnote not in footnotes:
            footnotes.append(footnote)
        return footnotes.index(footnote) + 1

    def get_footnotes(self, page):
        if not hasattr(page, "footnotes_list"):
            page.footnotes_list = []
        return page.footnotes_list
