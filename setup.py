#!/usr/bin/env python
import os
from setuptools import setup


def get_absolutepath(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    with open(get_absolutepath(fname), 'r') as f:
        return f.read()

setup(
    name='widgy-blog',
    version='0.1-dev',
    description=__doc__,
    long_description=read('README.rst'),
    packages=['widgy_blog'],
    include_package_data=True,
    install_requires=[
        'django-widgy',
    ],
    zip_safe=False,
)
