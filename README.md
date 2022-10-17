# Wagtail Footnotes

Add footnotes functionality to your Wagtail project.

## ⚡ Quick start

Add `wagtail_footnotes` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "wagtail_footnotes",
    ...
]
```

Add the footnotes `urls.py` to your project's `urls.py`:

```python
from wagtail_footnotes import urls as footnotes_urls
urlpatterns = [
    ...
    path("footnotes/", include(footnotes_urls)),
    ...
]
```

*Note: The URL has to be defined as above as it is currently hardcoded in the Javascript.*

Update your page models to show the footnotes panel:

```python
class InformationPage(Page):
    ...
    content_panels = [
        ...
        InlinePanel("footnotes", label="Footnotes"),
    ]
```

### Showing Footnotes in page templates

Update your page templates to include `{% include "wagtail_footnotes/includes/footnotes.html" %}`. You can copy from this template and instead include your own customized version.

### Using footnotes in RichTextField

Update any `RichTextField`s that you want to add footnotes feature. Add `"footnotes"` to the `features` arg for each `RichTextField` that you want to have this functionality. For instance:

```
class MyPage(Page):
    body = RichTextField(
        features=[
            "h1",
            "h2",
            "h3",
            "h4",
            "footnotes",  # Make sure this line is part of the features
        ],
    )

```

[See Wagtail's documentation](https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field) for a list of features that you may want to configure since we are overwriting the defaults.

### Using footnotes in `StreamField`s

In order to have footnotes available in a `RichTextBlock`, you will need to change `RichTextBlock`s to `wagtail_footnotes.blocks.RichTextBlockWithFootnotes`. For instance:

```python
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes
# ...
class MyPage(Page):
    body = StreamField(
        [
            # ...
            ("paragraph", RichTextBlockWithFootnotes()),  # Using RichTextBlockWithFootnotes
            # ...
        ],
    )
```

### Adding footnotes as a global default

You might want to simply have all RichText editors display footnotes. But remember that you will need the footnotes `InlinePanel` enabled on all your Page models for this to really make sense.

```python
# ...
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {"features": ["bold", "italic", "h3", "h4", "ol", "ul", "link", "footnotes"]},
    }
}
```

### 🏁 Finally, ALWAYS

After adding the footnotes app and making changes to your models, make and run migrations:

```
python manage.py makemigrations
python manage.py migrate
```

## ⚙️ Settings

 - `WAGTAIL_FOOTNOTES_TEXT_FEATURES`
   - Default: `["bold", "italic", "link"]`
   - Use this to update a list of Rich Text features allowed in the footnote text.

## 💡 Common issues
 - I click on the `Fn` button in the editor and it stops working
    - This is likely because the URL in the JS does not match the URL of the footnotes view. Check the URL in `wagtail_footnotes/static/footnotes/js/footnotes.js` matches the URL you set.
 - `NoneType` error when rendering page.
    - Make sure you are rendering the field in the template using `{% include_block page.field_name %}`
