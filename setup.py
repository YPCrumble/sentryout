#!/usr/bin/env python
"""
sentryout
======

Command line tool to write stdout/stderr to sentry.

"""

from setuptools import setup
import sentryout

setup(
    name='sentryout',
    version='.'.join(map(str, sentryout.VERSION)),
    author='Matt Oberle',
    author_email='matt.r.oberle@gmail.com',
    description='Command line tool to write stdout/stderr to sentry.',
    long_description=__doc__,
    py_modules = [
        "sentryout/main"
        ],
    packages = ["sentryout"],
    zip_safe=True,
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    scripts = ["scripts/sentryout"],
    url = "",
    install_requires = [
        'raven',
        ]
)

