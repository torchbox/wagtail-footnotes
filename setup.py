#!/usr/bin/env python

# from setuptools import setup

# # Redefine `name` here so GitHub’s "Used By" can detect the package.
# setup(name="wagtail-footnotes")


from os import path

from setuptools import find_packages, setup

from wagtail_footnotes import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail-footnotes",
    version=__version__,
    description="Add footnotes to rich text in your Wagtail pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cameron Lamb",
    author_email="cameron.lamb@torchbox.com",
    url="https://github.com/torchbox/wagtail-footnotes",
    packages=find_packages(exclude=["tests", "tests.*", "tests.*.*", "tests.*.*.*"]),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
    ],
    install_requires=["wagtail>=4.1"],
    extras_require={
        "testing": [
            "pre-commit>=3.3.0,<4",
            "tox==3.26.0",
        ],
    },
    zip_safe=False,
)
