from django.forms import HiddenInput
from wagtail import VERSION as WAGTAIL_VERSION


if WAGTAIL_VERSION >= (6, 0):
    from django.forms import Media
    from django.utils.safestring import mark_safe

    class ReadonlyUUIDInput(HiddenInput):
        """
        This isn't really read-only. It's a hidden input with an an adjacent div
        showing the current value; that way we can set the value in JavaScript, but
        the user can't easily change it.
        """

        def render_html(self, name, value, attrs):
            """Render the HTML (non-JS) portion of the field markup"""
            hidden = super().render(name, value, attrs)
            display_value = value[:6] if value is not None else value
            shown = f'<div id="{attrs["id"]}_display-value" style="padding-top: 1.2em;">{display_value}</div>'
            return mark_safe(shown + hidden)  # noqa: S308

        def render(self, name, value, attrs=None, renderer=None):
            # Ensure 'id' is present in attrs
            try:
                attrs["id"]
            except (KeyError, TypeError):
                raise TypeError(  # noqa: B904
                    "ReadonlyUUIDInput cannot be rendered without an 'id' attribute"
                )

            # Render the HTML portion
            widget_html = self.render_html(name, value, attrs)

            # Combine HTML and JavaScript, and mark as safe
            out = f"{widget_html}<script></script>"
            return mark_safe(out)  # noqa: S308

        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "read-only-uuid"
            return attrs

        @property
        def media(self):
            return Media(js=["js/custom-editor-controller.js"])

else:
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
