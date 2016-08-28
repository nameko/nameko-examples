#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-examples-orders',
    version='0.0.1',
    description='Store and serve orders',
    install_requires=[
        'nameko==2.3.1',
        'nameko-sqlalchemy==0.0.3',
        'alembic==0.8.7',
        'marshmallow==2.9.1'
    ],
    extras_require={
        'dev': [
            'pytest==2.9.2',
            'coverage==4.2'
        ],
    },
    zip_safe=True
)
