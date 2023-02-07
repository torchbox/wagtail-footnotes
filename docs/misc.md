# Misc. Info

This is were I am keeping notes for the moment.

## Useful scripts

Creating fixtures

```bash
python testmanage.py dumpdata wagtail_footnotes_test.TestPageStreamField --indent 2 > wagtail_footnotes/test/fixtures/page.json

python testmanage.py dumpdata wagtailcore.Page --indent 2 > wagtail_footnotes/test/fixtures/core.json

python testmanage.py dumpdata wagtail_footnotes --indent 2 > wagtail_footnotes/test/fixtures/footnotes.json

python testmanage.py dumpdata auth.user --indent 2 > wagtail_footnotes/test/fixtures/users.json
```

## Tox snippets

```bash
tox -e python3.9-django3.0-wagtail2.15
tox -e python3.9-django3.2-wagtail2.16
tox -e python3.10-django4.0-wagtail3.0
tox -e python3.10-django4.1-wagtail4.0
```
