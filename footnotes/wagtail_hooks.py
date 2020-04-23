import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.templatetags.static import static
from django.utils.html import format_html_join
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)
from wagtail.core import hooks


@hooks.register("insert_editor_js")
def editor_js():
    """ Includes uuidv4() function courtesy of
    https://stackoverflow.com/a/2117523/823020
    """
    js_files = [
        # We require this file here to make sure it is loaded before footnotes.js.
        "wagtailadmin/js/draftail.js",
        "footnotes/js/footnotes.js",
    ]
    js_includes = format_html_join(
        "\n",
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )
    return js_includes


@hooks.register("register_rich_text_features")
def register_footnotes_feature(features):
    """
    Registering the `footnotes` feature, which uses the `FOOTNOTES` Draft.js
    entity type, and is stored as HTML with a
    `<footnotes id="">short-id</footnotes>` tag.
    """
    feature_name = "footnotes"
    type_ = "FOOTNOTES"

    control = {"type": type_, "label": "Fn", "description": "Footnotes"}

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            control,
            # The JS for footnotes would have been passed here, see above.
        ),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                "footnote[id]": FootnotesEntityElementHandler(type_)
            },
            "to_database_format": {
                "entity_decorators": {type_: footnotes_entity_decorator}
            },
        },
    )


def footnotes_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the FOOTNOTES entities into a footnote tag.
    """
    return DOM.create_element("footnote", {"id": props["footnote"]}, props["children"])


class FootnotesEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the footnote tag into a FOOTNOTES entity, with the right data.
    """

    mutability = "IMMUTABLE"

    def get_attribute_data(self, attrs):
        """
        Take the ``footnote UUID`` value from the ``id`` HTML attribute.
        """
        return {"footnote": attrs["id"]}
