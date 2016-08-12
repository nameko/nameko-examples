#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='gateway-service',
    version='0.0.1',
    description='Gateway for Airships ltd',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "nameko==2.3.1",
    ],
    extras_require={
        'dev': [
            "pytest==2.4.2",
            "coverage==4.0a1",
            "isort==4.0.0"
        ],
    },
    zip_safe=True
)
