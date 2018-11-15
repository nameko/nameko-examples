#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-examples-gateway',
    version='0.0.1',
    description='Gateway for Airships ltd',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "marshmallow==2.15.1",
        "nameko==2.8.5",
    ],
    extras_require={
        'dev': [
            'pytest==3.1.1',
            'coverage==4.4.1',
            'flake8==3.3.0'
        ],
    },
    zip_safe=True
)
