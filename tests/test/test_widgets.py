from django import forms
from django.test import TestCase

from wagtail_footnotes.widgets import ReadonlyUUIDInput


class TestWidgets(TestCase):
    def test_read_only_uuid_input(self):
        form = forms.Form()
        form.fields["uuid"] = forms.CharField(widget=ReadonlyUUIDInput)

        self.assertInHTML(
            '<input type="hidden" name="uuid" id="id_uuid" data-controller="read-only-uuid">',
            form.as_p(),
        )

    def test_display_value_div_rendered_with_correct_id(self):
        """The display div must use the predictable ID pattern `{input_id}_display-value`.

        This ID is load-bearing: the "Create new footnote" JS stamps the UUID
        into it (Feature 1) and the "Go to reference" back-link is inserted
        immediately after it (Feature 3). If the ID format changes, both
        features silently break.
        """
        widget = ReadonlyUUIDInput()
        html = widget.render(
            "uuid", "f291a4b7-5ac5-4030-b341-b1993efb2ad2", attrs={"id": "id_uuid"}
        )

        self.assertIn('id="id_uuid_display-value"', html)

    def test_display_value_shows_first_six_chars_of_uuid(self):
        """The visible display truncates the UUID to 6 chars — matching the
        short key used in the Draftail editor and the chooser modal table."""
        from bs4 import BeautifulSoup

        widget = ReadonlyUUIDInput()
        full_uuid = "f291a4b7-5ac5-4030-b341-b1993efb2ad2"
        html = widget.render("uuid", full_uuid, attrs={"id": "id_uuid"})

        soup = BeautifulSoup(html, "html.parser")
        display_div = soup.find("div", {"id": "id_uuid_display-value"})
        self.assertIsNotNone(display_div)
        self.assertEqual(display_div.text, "f291a4")
