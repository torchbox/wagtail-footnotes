from django import template

register = template.Library()


@register.simple_tag()
def footnotes_in_page(page):
    """
    Return a unique list of the footnotes for the given page,
    preserving the order that they appear in.
    """
    if hasattr(page, "footnotes_list"):
        # Track if we have seen the footnote in the list yet.
        seen = set()
        seen_add = seen.add
        return [x for x in page.footnotes_list if not (x in seen or seen_add(x))]
    return []
