#!/usr/bin/env python

from setuptools import setup,find_packages



setup(
    name='django-copy',
    version='0.1',
    description='Extremely simple CMS for Django',
    long_description="Probably the smallest and simplest CMS for Django.",
    keywords='django, cms',
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
