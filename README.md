# Wagtail Footnotes

This repo contains example code that can be copied and altered to add footnotes to your wagtail pages.

## Usage
 - Copy the `/footnotes` directory into your project
 - Add the app to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       ...
       "projectname.footnotes",
       ...
   ]
   ```
 - Update the migrations in `projectname/footnotes/migrations` to point at the app:
   ```python
   import projectname.footnotes.fields
   projectname.footnotes.fields.CustomUUIDField
   ...
 - Add the footnotes `urls.py` to your project's `urls.py`:
   ```python
   from projectname.footnotes import urls as footnotes_urls
   private_urlpatterns = [
       ...
       path("footnotes/", include(footnotes_urls)),
       ...
   ]
   ```
 - Update your page models to use the `FootnotesMixin`:
   ```python
   from projectname.footnotes.models import FootnotesMixin
   class InformationPageRelatedPage(RelatedPage, FootnotesMixin):
        ...
        content_panels = BasePage.content_panels + [
            ...
        ] + FootnotesMixin.footnote_panels
   ```
 - Update your `RichTextBlock`s 
    - Add `"footnotes"` to the `features` arg for each `RichTextBlock` that you want to have this functionality.
    - You will also need to change them from `RichTextBlock`s to `projectname.footnotes.blocks.RichTextBlockWithFootnotes`
    - You can add the footnotes to `RichTextBlock`s across the project by updating `WAGTAILADMIN_RICH_TEXT_EDITORS["default"]["OPTIONS"]["features"]`:
      ```python
       WAGTAILADMIN_RICH_TEXT_EDITORS = {
            "default": {
                "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
                "OPTIONS": {"features": ["bold", "italic", "h3", "h4", "ol", "ul", "link", "footnotes"]},
            }
        }
      ```
 - Update your page templates to include `{% include "footnotes/includes/footnotes.html" %}`
 - Make and run migrations:
   ```
   ./manage.py makemigrations
   ./manage.py migrate
   ```

## Common issues
 - I click on the `Fn` button in the editor and it stops working
    - This is likely because the URL in the JS does not mathc the URL of the footnotes view. Check the URL in `projectname/footnotes/static/footnotes/js/footnotes.js` matches the URL you set.
