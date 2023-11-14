# Wagtail Footnotes

[![PyPI](https://img.shields.io/pypi/v/wagtail-footnotes.svg)](https://pypi.org/project/wagtail-footnotes/)
[![PyPI downloads](https://img.shields.io/pypi/dm/wagtail-footnotes.svg)](https://pypi.org/project/wagtail-footnotes/)
[![Build Status](https://github.com/torchbox/wagtail-footnotes/workflows/CI/badge.svg)](https://github.com/torchbox/wagtail-footnotes/actions)

Add footnotes functionality to your Wagtail project.

## Usage

- Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_footnotes",
    # ...
]
```

- Add the footnotes `urls.py` to your project's `urls.py`:

```python
from wagtail_footnotes import urls as footnotes_urls

urlpatterns = [
    # ...
    path("footnotes/", include(footnotes_urls)),
    # ...
]
```

Note: The URL has to be defined as above as it is currently hardcoded in the Javascript.

- Update your page models to show the footnotes field:

```python
class InformationPage(BasePage):
    # ...
    content_panels = [
        # ...
        InlinePanel("footnotes", label="Footnotes"),
    ]
```

- Update your `RichTextBlock`s
  - Add `"footnotes"` to the `features` arg for each `RichTextBlock` that you want to have this functionality
  - You will also need to change any `RichTextBlock`s to `wagtail_footnotes.blocks.RichTextBlockWithFootnotes`
- Update your page templates to include `{% include "wagtail_footnotes/includes/footnotes.html" %}`

Make and run migrations:

```bash
./manage.py makemigrations
./manage.py migrate
```

## Settings

- `WAGTAIL_FOOTNOTES_TEXT_FEATURES`
  - Default: `["bold", "italic", "link"]`
  - Use this to update a list of Rich Text features allowed in the footnote text.

## Common issues

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
pip install -e '.[testing]' -U
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit). To set up locally:

```shell
$ pip install pre-commit
# initialize pre-commit
$ pre-commit install
# Optional, run all checks once for this, then the checks will run only on the changed files
$ pre-commit run --all-files
```

### How to run tests

To run all tests in all environments:

```sh
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
