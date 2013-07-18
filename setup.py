#!/usr/bin/env python
import os
from setuptools import setup, find_packages

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
    install_requires=[
        'django-fusionbox',
        'widgy',
    ],
    dependency_links=[
        'http://github.com/fusionbox/django-fusionbox/tarball/master#egg=django-fusionbox-0.0.2',
        'http://github.com/fusionbox/django-widgy/tarball/master#egg=widgy-0.0.1',
    ],
    zip_safe=False,
)
