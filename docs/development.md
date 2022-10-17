# Develop Wagtail Footnotes

- [Index](./index.md)

## Setup

### Create and activate virtual environment

Example:

```bash
pyenv virtualenv wagtail-footnotes
pyenv activate wagtail-footnotes
```

Then run:

```bash
pip install ".[testing]"
pip install -r requirements-dev.txt
python testmanage.py migrate
python testmanage.py runserver 0.0.0.0:8000
```

Now you can view the test site at `http://localhost:8000`

**To access the admin area** first create a superuser account.

```bash
python testmanage.py createsuperuser
```

Access the Wagtail admin at `http://localhost:8000/admin` and login using the account you just created.
