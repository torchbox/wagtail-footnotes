from django.test import TestCase

from wagtail_footnotes.fields import CustomUUIDField


class TestFields(TestCase):
    def test_custom_uuid_field(self):
        uuid_field = CustomUUIDField()
        self.assertEqual(
            uuid_field.from_db_value(
                "12345678-1234-5678-1234-567812345678", None, None
            ),
            "12345678-1234-5678-1234-567812345678",
        )
