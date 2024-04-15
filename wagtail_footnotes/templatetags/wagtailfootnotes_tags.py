from django import template


register = template.Library()


@register.filter
def get_reference_ids(value, footnote_uuid):
    """This takes the current `footnote_uuid` and returns the list of references in the page content to that footnote.
    This template tag is only necessary because it is not possible to do dictionary lookups using variables as keys in
    Django templates.
    """
    if hasattr(value, "footnotes_references"):
        return value.footnotes_references.get(footnote_uuid, [])
    return []
