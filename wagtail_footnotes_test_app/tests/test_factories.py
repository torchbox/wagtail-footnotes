from django.test import TestCase

from ..factories import TestPage


class TestPageFactory(TestCase):
    def test_testpage_factory(self):
        TestPage()

    def test_testpage_factory_with_empty_body(self):
        TestPage(body={})
