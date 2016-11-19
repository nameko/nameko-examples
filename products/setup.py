#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-examples-products',
    version='0.0.1',
    description='Products - Nameko service example',
    author='nameko',
    url='http://github.com/nameko/nameko-examples/products',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['products'],
    install_requires=[
        "nameko>=2.4.2",
    ],
    extras_require={
        'dev': [
            "coverage==4.2",
            "flake8==3.0.4",
            "pytest==3.0.3",
        ]
    },
    zip_safe=True,
)
