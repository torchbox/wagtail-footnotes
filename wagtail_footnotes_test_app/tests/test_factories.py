from django.test import TestCase

from .. import factories


class TestPageFactory(TestCase):
    def test_factory(self):
        factories.TestPage()

    def test_factory_with_empty_body(self):
        factories.TestPage(body={})
