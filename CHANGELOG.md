# Wagtail Footnotes Changelog

## 0.9.0

- Add support for Wagtail 4.0
- Add GitHub Action to publish to PyPI on release by @zerolab in https://github.com/torchbox/wagtail-footnotes/pull/45

## 0.8.0

 - Add support for Wagtail 3.0 and drop support for all Wagtail versions
   before 2.15
 - Dropped support for all Django versions
   before 3.2
 - Removed support for Python 3.6
 - Fix previews https://github.com/torchbox/wagtail-footnotes/pull/24 - [@jsma](https://github.com/jsma)

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
