# TODO:
#  - Create a Page with a footnote
#  - Render a Page with a footnote
#  - Check the rendered page for the footnote output
#  - Check the rendered page for the footnote listing
#  - Try saving a page where the footnote's ID is None
#  - Try saving a page where the rich text references a footnote that no longer exists

import wagtail_factories

from django.test import TestCase

from wagtail.core.rich_text import RichText

from .. import factories


class Footnotes(TestCase):
    def setUp(self):
        # Build home page and default site
        self.root_page = wagtail_factories.PageFactory(parent=None)
        self.site = wagtail_factories.SiteFactory(
            is_default_site=True, root_page=self.root_page
        )

    def test_create_page_with_footnote(self):
        # Build a page
        rich_text = RichText("test")
        page = factories.TestPage(
            parent=self.root_page,
            body__0__paragraph__value=rich_text,
        )
        # Render the page
        response = self.client.get(page.url)
        # Test the response
        self.assertEquals(response.status_code, 200)
