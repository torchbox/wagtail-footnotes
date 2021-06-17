from django.test import TestCase

from .. import factories


class TestPageFactory(TestCase):
    def test_factory(self):
        factories.TestPage()

    def test_factory_with_empty_body(self):
        factories.TestPage(body={})


# TODO:
#  - Create a Page with a footnote
#  - Render a Page with a footnote
#  - Check the rendered page for the footnote output
#  - Check the rendered page for the footnote listing
#  - Try saving a page where the footnote's ID is None
#  - Try saving a page where the rich text references a footnote that no longer exists
