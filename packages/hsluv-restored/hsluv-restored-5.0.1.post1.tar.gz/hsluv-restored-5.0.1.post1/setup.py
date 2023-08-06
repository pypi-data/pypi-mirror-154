#!/usr/bin/python
from setuptools import setup

from hsluv import __version__

setup(
    name='hsluv-restored',
    version=__version__+'.post1',
    description='Human-friendly HSL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    author_email="alexei@boronine.com",
    url="https://www.hsluv.org",
    keywords="color hsl cie cieluv colorwheel hsluv hpluv",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    setup_requires=[
        'setuptools>=38.6.0',  # for long_description_content_type
    ],
    py_modules=["hsluv"],
    test_suite="tests.test_hsluv"
)
