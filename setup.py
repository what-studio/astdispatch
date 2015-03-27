# -*- coding: utf-8 -*-
"""
"""
from __future__ import with_statement
import re
from setuptools import setup
from setuptools.command.test import test


# detect the current version
with open('astdispatch.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead
def run_tests(self):
    raise SystemExit(__import__('pytest').main(['-v']))
test.run_tests = run_tests


setup(
    name='astdispatch',
    version=version,
    license='BSD',
    author='What! Studio',
    maintainer='Heungsub Lee',
    maintainer_email='sub@nexon.co.kr',
    url='https://github.com/what-studio/astdispatch',
    description='Visits AST nodes by singledispatch-like API',
    long_description=__doc__,
    platforms='any',
    py_modules=['astdispatch'],
    classifiers=[],
    install_requires=['singledispatch'],
    tests_require=['astunparse', 'pytest'],
    test_suite='...',
)
