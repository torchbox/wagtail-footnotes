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
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
    ],
    install_requires=["wagtail>=2.15, <5.0"],
    extras_require={
        "testing": ["dj-database-url==0.5.0"],
    },
    zip_safe=False,
)
