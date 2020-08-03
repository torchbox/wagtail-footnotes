from django.forms import HiddenInput
from wagtail.utils.widgets import WidgetWithScript


class ReadonlyUUIDInput(WidgetWithScript, HiddenInput):
    """
    This isn't really read-only. It's a hidden input with an an adjacent div
    showing the current value; that way we can set the value in JavaScript, but
    the user can't easily change it.
    """

    def render_html(self, name, value, attrs):
        """Render the HTML (non-JS) portion of the field markup"""
        hidden = super(WidgetWithScript, self).render(name, value, attrs)
        display_value = value[:6] if value is not None else value
        shown = f'<div id="{attrs["id"]}_display-value" style="padding-top: 1.2em;">{display_value}</div>'
        return shown + hidden

    def render_js_init(self, id_, name, value):
        return f'setUUID("{id_}");'
