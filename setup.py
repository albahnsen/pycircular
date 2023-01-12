#!/usr/bin/env python

from setuptools import setup, find_packages
import re

for line in open('pycircular/__init__.py'):
    match = re.match("__version__ *= *'(.*)'", line)
    if match:
        __version__, = match.groups()

setup(
    name='pycircular',
    version=__version__,
    license='new BSD',
    long_description=open('README.rst').read(),
    author="Alejandro Correa Bahnsen",
    author_email='al.bahnsen@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    keywords=['machine learning', 'circular', 'feature engineering'],
    url='https://github.com/albahnsen/pycircular',
    install_requires=['scikit-learn', 'pandas'],
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.9',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent'],
)