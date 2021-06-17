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

    def test_create_page_with_footnotes(self):
        footnote1 = factories.Footnote()
        footnote2 = factories.Footnote()
        footnote3 = factories.Footnote()
        # Build a page with footnotes
        rich_text = RichText(
            f"{create_footnote_tag(footnote1.uuid)}"
            f"{create_footnote_tag(footnote2.uuid)}"
            f"{create_footnote_tag(footnote3.uuid)}"
        )
        page = factories.TestPage(
            parent=self.root_page,
            body__0__paragraph__value=rich_text,
        )
        footnote1.page = page
        footnote1.save()
        footnote2.page = page
        footnote2.save()
        footnote3.page = page
        footnote3.save()
        # Render the page
        response = self.client.get(page.url)
        # Test the response
        self.assertEquals(response.status_code, 200)
        # Check for the footnote
        self.assertContains(response, 'id="footnote-source-1"')
        self.assertContains(response, 'id="footnote-source-2"')
        self.assertContains(response, 'id="footnote-source-3"')
        # Check for the footnote list
        self.assertContains(response, footnote1.text)
        self.assertContains(response, footnote2.text)
        self.assertContains(response, footnote3.text)
        # TODO: Check order of footnotes in list matches order in rich_text
