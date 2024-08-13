# Wagtail Footnotes Changelog

## Unreleased

## 0.12.0

- Added support for Wagtail 6.2 (https://github.com/torchbox/wagtail-footnotes/pull/72) @willbarton
  Note: this adds a backwards-compatible locale verbose_name migration
- Added ability to customize the footnote reference rendering (https://github.com/torchbox/wagtail-footnotes/pull/70) @willbarton
  To change the default template (`wagtail_footnotes/includes/footnote_reference.html`), add the `WAGTAIL_FOOTNOTES_REFERENCE_TEMPLATE` setting to your template

## 0.11.0

- Improve README @benjaoming
- Drop support for Wagtail < 5.2 @katdom13
- Add support for Wagtail 6.0/6.1, Django 5.0 and Python 3.12 @katdom13
- Make footnotes translatable @jhonatan-lopes, and make the package strings translatable @zerolab

## 0.10.0

- Add tests. (https://github.com/torchbox/wagtail-footnotes/pull/49) @nickmoreton
  Includes tox 4, coverage configuration.
- Drop support for Python 3.7 and Wagtail < 4.1. (https://github.com/torchbox/wagtail-footnotes/pull/49) @nickmoreton
- Add the coverage report to the GitHub Actions summary. @zerolab
- Switch to using [ruff](https://beta.ruff.rs/docs/) for linting. (https://github.com/torchbox/wagtail-footnotes/pull/52) @zerolab
- Switched to using PyPI trusted publishing (https://github.com/torchbox/wagtail-footnotes/pull/53) @zerolab
- Switched to using [flit](https://flit.pypa.io/en/latest/) for packaging (https://github.com/torchbox/wagtail-footnotes/pull/54) @zerolab

## 0.9.0

- Add support for Wagtail 4.0
- Add GitHub Action to publish to PyPI on release by @zerolab in (https://github.com/torchbox/wagtail-footnotes/pull/45)

## 0.8.0

- Add support for Wagtail 3.0 and drop support for all Wagtail versions before 2.15
- Dropped support for all Django versions before 3.2
- Removed support for Python 3.6
- Fix previews (https://github.com/torchbox/wagtail-footnotes/pull/24) - [@jsma](https://github.com/jsma)

## 0.7.0

- Clean up old step from README - It is no longer recommended to define footnotes in `WAGTAILADMIN_RICH_TEXT_EDITORS`
- Add `footnotes` rich text feature automatically
- Clean up `RichTextBlockWithFootnotes`
- Make Footnotes unique on `page` <-> `uuid`

## 0.6.0

- Add `WAGTAIL_FOOTNOTES_TEXT_FEATURES` to add custom rich text features to footnote content
- Update requrements to `Django>=2.2, <3.3`

## 0.5.0

- Update requirements to `wagtail>=2.5, <3`
- Fix Javascript registering

## 0.4.0

- Replace tags in both `render` and `render_basic`

## 0.3.1

- Cleanup code/readme
- Increase requirements to `Django>=2.2, <3.2` and `wagtail>=2.5, <2.11`

## 0.3.0

- Remove old template tag references
- Remove the `FootnotesMixin`
- Mark output of `RichTextBlockWithFootnotes` as safe

## 0.2.0

- Moved templates to `wagtail_footnotes/templates/wagtail_footnotes/*`

## 0.1.0

- Initial release of the Wagtail Footnotes package
