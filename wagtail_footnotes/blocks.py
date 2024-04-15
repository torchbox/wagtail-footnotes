import re

from collections import defaultdict

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.blocks import RichTextBlock
from wagtail.models import Page


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
        self.footnotes = {}

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
        if not hasattr(page, "footnotes_references"):
            page.footnotes_references = defaultdict(list)
        self.footnotes = {
            str(footnote.uuid): footnote for footnote in page.footnotes.all()
        }

        def replace_tag(match):
            footnote_uuid = match.group(1)
            try:
                index = self.process_footnote(footnote_uuid, page)
            except (KeyError, ValidationError):
                return ""
            else:
                # Generate a unique html id for each link in the content to this footnote since the same footnote may be
                # referenced multiple times in the page content. For the first reference to the first footnote, it will
                # be "footnote-source-1-0" (the index for the footnote is 1-based but the index for the links are
                # 0-based) and if it's the second link to the first footnote, it will be "footnote-source-1-1", etc.
                # This ensures the ids are unique throughout the page and allows for the template to generate links from
                # the footnote back up to the distinct references in the content.
                link_id = f"footnote-source-{index}-{len(page.footnotes_references[footnote_uuid])}"
                page.footnotes_references[footnote_uuid].append(link_id)
                return f'<a href="#footnote-{index}" id="{link_id}"><sup>[{index}]</sup></a>'

        # note: we return safe html
        return mark_safe(FIND_FOOTNOTE_TAG.sub(replace_tag, html))  # noqa: S308

    def render(self, value, context=None):
        kwargs = {"value": value} if WAGTAIL_VERSION >= (5, 2) else {}

        if not self.get_template(context=context, **kwargs):
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
