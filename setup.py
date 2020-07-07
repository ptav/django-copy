#!/usr/bin/env python
import os
from setuptools import setup,find_packages

PATH = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PATH, 'README.md'), encoding='utf-8') as fp:
    DESC = fp.read()


setup(
    name='django-copy',
    version='1.1',
    description='Probably the smallest and simplest CMS for the Django framework',
    long_description=DESC,
    keywords='Django, CMS',
    author='Pedro Tavares',
    author_email='web@ptavares.com',
    url='https://github.com/ptav/django-copy',
    license='LICENSE',

    packages=find_packages(),
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
