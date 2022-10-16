# Develop Wagtail Footnotes

- [Index](./index.md)

## Setup

### Create and activate virtual environment.

In a bash console and run

```bash
pyenv virtualenv wagtail-footnotes
pyenv activate wagtail-footnotes
```

Then run commands from the Makefile

```bash
make install
make setup
```

This will install and run some initial data and end with the local development server running at `http://localhost:8000`

You can access the Wagtail admin at `http://localhost:8000` and login using

- Username: `admin`
- Password: `password`

## Running Tests

In a bash console run:

```bash
make test
```

The test will be run on the latest Wagtail and Django releases.

### Running Tox

To run all tests on all versions run:

```bash
tox
```

To run tests on specific Wagtail versions run:

```bash
make 215 # Wagtail 2.15
make 216 # Wagtail 2.16
make 30 # Wagtail 3.0
make 40 # Wagtail 4.0
