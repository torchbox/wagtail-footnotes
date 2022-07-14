# Wagtail Footnotes

[![PyPI](https://img.shields.io/pypi/v/wagtail-footnotes.svg)](https://pypi.org/project/wagtail-footnotes/)
[![PyPI downloads](https://img.shields.io/pypi/dm/wagtail-footnotes.svg)](https://pypi.org/project/wagtail-footnotes/)
[![Build Status](https://github.com/torchbox/wagtail-footnotes/workflows/CI/badge.svg)](https://github.com/torchbox/wagtail-footnotes/actions)

Add footnotes functionality to your Wagtail project.

## ⚡ Quick start

Add `wagtail_footnotes` to `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "wagtail_footnotes",
    # ...
]
```

Add the footnotes `urls.py` to your project's `urls.py`:

```python
# urls.py
# ...
from wagtail_footnotes import urls as footnotes_urls


urlpatterns = [
    # ...
    path("footnotes/", include(footnotes_urls)),
    # ...
]
```

*Note*: The URL has to be defined as above as it is currently hardcoded in the JavaScript.

Update your page models to show the footnotes panel:

```python
from wagtail.models import Page
from wagtail.admin.panels import InlinePanel


class InformationPage(Page):
    # ...
    content_panels = [
        # ...
        InlinePanel("footnotes", label="Footnotes"),
    ]
```

Make and run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Showing footnotes in page templates

Update your page templates to include `{% include "wagtail_footnotes/includes/footnotes.html" %}`. You can copy from this template and instead include your own customized version.

### Using footnotes in `RichTextField`

Update any `RichTextField`s that you want to add footnotes feature. 
Add `"footnotes"` to the `features` argument for each `RichTextField` that you want to have this functionality. For instance:

```
class InformationPage(Page):
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

You might want to simply have all RichText editors display footnotes. But remember that you will need the footnotes `InlinePanel` added 
on all your Page models for the footnotes functionality to be enabled.

```python
# settings.py
# ...
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {"features": ["bold", "italic", "h3", "h4", "ol", "ul", "link", "footnotes"]},
    }
}
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

## Contributing

All contributions are welcome!

### Install

To make changes to this project, first clone this repository:

```sh
git clone git@github.com:torchbox/wagtail-footnotes.git
cd wagtail-footnotes
```

With your preferred virtualenv activated, install testing dependencies:

```sh
python -m pip install -e '.[testing]' -U
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit). To set up locally:

```shell
# set up your virtual environment of choice
$ python -m pip install pre-commit
# initialize pre-commit
$ pre-commit install
# Optional, run all checks once for this, then the checks will run only on the changed files
$ pre-commit run --all-files
```

### How to run tests

To run all tests in all environments:

```shell
tox
```

To run tests for a specific environment:

```shell
tox -e python3.11-django4.2-wagtail5.2
```

To run a single test method in a specific environment:

```shell
tox -e python3.11-django4.2-wagtail5.2 -- tests.test.test_blocks.TestBlocks.test_block_with_features
```
