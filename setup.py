#!/usr/bin/env python
import os
import sys

from setuptools import setup

version = "1.0"

setup(
    name = "CatmanReader",
    version = "1.0",
    author = "Carlos Rubio",
    description = ("Binary reader for Catman v5+ files"),
    license = "MIT",
    keywords = "catman data file reader",
    packages = ['catman'],
    install_requires=[]
)
