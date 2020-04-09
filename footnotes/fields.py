from django.db.models import UUIDField


class CustomUUIDField(UUIDField):
    """ Returns database value as a string, so that dashes are preserved. """

    def from_db_value(self, value, expression, connection, context):
        return str(value)
