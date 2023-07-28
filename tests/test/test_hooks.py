from django.test import TestCase

from wagtail_footnotes.wagtail_hooks import (
    FootnotesEntityElementHandler,
    footnotes_entity_decorator,
)


class TestHooks(TestCase):
    def test_footnotes_entity_decorator(self):
        props = {"footnote": "1", "children": ""}
        dom = footnotes_entity_decorator(props)
        self.assertEqual(dom.type, "footnote")
        self.assertEqual(dom.children, [])

    def test_footnotes_entity_decorator_with_children(self):
        props = {"footnote": "1", "children": "This is a footnote"}
        dom = footnotes_entity_decorator(props)
        self.assertEqual(dom.type, "footnote")
        self.assertEqual(dom.children, ["This is a footnote"])

    def test_footnotes_entity_element_handler(self):
        attrs = {"id": "1ahyt67", "footnote": "1"}
        element = FootnotesEntityElementHandler(attrs)
        self.assertEqual(element.get_attribute_data(attrs), {"footnote": "1ahyt67"})
