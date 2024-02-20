from django import forms
from django.test import TestCase
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_footnotes.widgets import ReadonlyUUIDInput


class TestWidgets(TestCase):
    def test_read_only_uuid_input(self):
        form = forms.Form()
        form.fields["uuid"] = forms.CharField(widget=ReadonlyUUIDInput)

        if WAGTAIL_VERSION >= (6, 0):
            self.assertInHTML(
                '<input type="hidden" name="uuid" id="id_uuid" data-controller="read-only-uuid">',
                form.as_p(),
            )
        else:
            self.assertInHTML(
                '<input type="hidden" name="uuid" id="id_uuid">',
                form.as_p(),
            )
            self.assertInHTML(
                '<script>setUUID("id_uuid");</script>',
                form.as_p(),
            )
