from django import forms
from django.test import TestCase

from wagtail_footnotes.widgets import ReadonlyUUIDInput


class TestWidgets(TestCase):
    def test_read_only_uuid_input(self):
        form = forms.Form()
        form.fields["uuid"] = forms.CharField(widget=ReadonlyUUIDInput)
        self.assertInHTML(
            '<input type="hidden" name="uuid" id="id_uuid">',
            form.as_p(),
        )
        self.assertInHTML(
            '<script>setUUID("id_uuid");</script>',
            form.as_p(),
        )
