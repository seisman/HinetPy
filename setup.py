#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='HinetPy',
    version='0.3.2',

    description='A NIED Hi-net web service client '
                'and win32 tools for seismologists.',
    long_description=long_description,

    url='https://github.com/seisman/HinetPy',

    author='Dongdong Tian',
    author_email='seisman.info@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    keywords='NIED Hi-net related tasks',
    packages=['HinetPy'],
    install_requires=['requests'],
    license='MIT',
)
