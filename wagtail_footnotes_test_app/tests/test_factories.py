from ..factories import TestPage


def test_testpage_factory():
    TestPage()


def test_testpage_factory_with_empty_body():
    TestPage(bady={})
