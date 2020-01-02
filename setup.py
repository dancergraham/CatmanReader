#!/usr/bin/env python
import os
import sys

from setuptools import setup

version = "1.2"

setup(
    name = "CatmanReader",
    version = version,
    author = "Carlos Rubio",
    description = ("Binary reader for Catman v5+ files"),
    license = "MIT",
    keywords = "catman data file reader",
    packages = ['catman'],
    install_requires=[]
)
