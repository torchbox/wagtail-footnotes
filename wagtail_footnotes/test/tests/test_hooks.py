from django.test import TestCase

from wagtail_footnotes.wagtail_hooks import footnotes_entity_decorator

class TestHooks(TestCase):
    # This is just to get a relatively simple test in place to get the ball rolling.
    def test_footnotes_entity_decorator(self):
        props = {
            "footnote": "1",
            "children": ""
        }
        dom = footnotes_entity_decorator(props)
        self.assertEqual(dom.type, "footnote")
