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


try:
    from functools import singledispatch
except ImportError:
    requirements = ['singledispatch']
else:
    del singledispatch
    requirements = []


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
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy'],
    install_requires=requirements,
    tests_require=['astunparse', 'pytest'],
    test_suite='...',
)
