#!/usr/bin/env python
import os
from setuptools import setup

from widgy_blog.version import get_version

__doc__ = "Reusable blog app for Django-Widgy"


def get_absolutepath(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    with open(get_absolutepath(fname), 'r') as f:
        return f.read()

setup(
    name='widgy-blog',
    version=get_version(),
    author='Fusionbox, Inc.',
    author_email='programmers@fusionbox.com',
    description=__doc__,
    long_description='\n\n'.join([read('README.rst'), read('CHANGES.rst')]),
    url='https://github.com/fusionbox/django-widgy-blog/',
    license='BSD',
    packages=['widgy_blog'],
    include_package_data=True,
    install_requires=[
        'django-widgy',
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
