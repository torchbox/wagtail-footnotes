# TODO:
#  - Create a Page with a footnote (Wagtail admin tests?)
#  - Try saving a page where the footnote's ID is None (Wagtail admin tests?)
#  - Try saving a page where the rich text references a footnote that no longer exists (Wagtail admin tests?)

import wagtail_factories

from django.test import TestCase

from wagtail.core.rich_text import RichText

from .. import factories


def create_footnote_tag(footnote_id):
    return f'<footnote id="{footnote_id}">footnote</footnote>'


class Footnotes(TestCase):
    def setUp(self):
        # Build home page and default site
        self.root_page = wagtail_factories.PageFactory(parent=None)
        self.site = wagtail_factories.SiteFactory(
            is_default_site=True, root_page=self.root_page
        )

    def test_create_page_with_footnote(self):
        footnote = factories.Footnote()
        # Build a page with a footnote
        rich_text = RichText(create_footnote_tag(footnote.uuid))
        page = factories.TestPage(
            parent=self.root_page,
            body__0__paragraph__value=rich_text,
        )
        footnote.page = page
        footnote.save()
        # Render the page
        response = self.client.get(page.url)
        # Test the response
        self.assertEquals(response.status_code, 200)
        # Check for the footnote (1, because it is the first on the page)
        self.assertContains(response, 'id="footnote-source-1"')
        # Check for the footnote list
        self.assertContains(response, footnote.text)
