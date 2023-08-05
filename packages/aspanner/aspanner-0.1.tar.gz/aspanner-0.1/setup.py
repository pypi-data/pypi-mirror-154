#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Aspanner
"""

from setuptools import setup

version = [i for i in open("aspanner/__init__.py").readlines() if i.startswith("__version__")][0]
__version__ = ''
exec(version)

setup(
  name="aspanner",
  version=__version__,
  keywords=['spanner', 'database', 'asyncio'],
  description="Asyncio Client for Google-Spanner, wrapped google-cloud-spanner.",

  author="LovinJoy",
  author_email='technical-committee@lovinjoy.com',
  url="http://github.com/LovinJoy-TC/aspanner",
  license="MIT License",
  install_requires=[
      'google-cloud-spanner>=3.14.0',
    ],
  packages=["aspanner"],
  # packages = find_packages(),
  python_requires='>=3.8',
)
