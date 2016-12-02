#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-examples-gateway',
    version='0.0.1',
    description='Gateway for Airships ltd',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "nameko==2.4.2",
        'kombu==3.0.37',
    ],
    extras_require={
        'dev': [
            'pytest==3.0.3',
            'coverage==4.2',
            'flake8==3.0.4'
        ],
    },
    zip_safe=True
)
