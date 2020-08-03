# Wagtail Footnotes

This repo contains example code that can be copied and altered to add footnotes to your wagtail pages.

## Usage
 - Add the app to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       ...
       "wagtail_footnotes",
       ...
   ]
   ```
 - Add the footnotes `urls.py` to your project's `urls.py`:
   ```python
   from wagtail_footnotes import urls as footnotes_urls
   urlpatterns = [
       ...
       path("footnotes/", include(footnotes_urls)),
       ...
   ]
   ```
   Note: The URL NEEDS to be defined as above as it is currently hardcoded in the JS
 - Update your page models to use the `FootnotesMixin`:
   ```python
   from wagtail_footnotes.models import FootnotesMixin
   class InformationPage(BasePage, FootnotesMixin):
        ...
        content_panels = [
            ...
        ] + FootnotesMixin.footnote_panels
   ```
 - Update your `RichTextBlock`s 
    - Add `"footnotes"` to the `features` arg for each `RichTextBlock` that you want to have this functionality.
    - You will also need to change them from `RichTextBlock`s to `wagtail_footnotes.blocks.RichTextBlockWithFootnotes`
    - You can add the footnotes to `RichTextBlock`s across the project by updating `WAGTAILADMIN_RICH_TEXT_EDITORS["default"]["OPTIONS"]["features"]`:
      ```python
      WAGTAILADMIN_RICH_TEXT_EDITORS = {
          "default": {
              "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
              "OPTIONS": {"features": ["bold", "italic", "h3", "h4", "ol", "ul", "link", "footnotes"]},
          }
      }
      ```
 - Update your page templates to include `{% include "wagtail_footnotes/includes/footnotes.html" %}`
 - Make and run migrations:
   ```
   ./manage.py makemigrations
   ./manage.py migrate
   ```

## Example implementations
 - Merge Request: https://git.torchbox.com/wharton/whartoninteractive/-/merge_requests/195
    - Initial commit: https://git.torchbox.com/wharton/whartoninteractive/-/commit/d368d59d34743dd6164b54c83b86d2e1f3bb8e62

## Common issues
 - I click on the `Fn` button in the editor and it stops working
    - This is likely because the URL in the JS does not match the URL of the footnotes view. Check the URL in `wagtail_footnotes/static/footnotes/js/footnotes.js` matches the URL you set.
