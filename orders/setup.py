#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-examples-orders',
    version='0.0.1',
    description='Store and serve orders',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'nameko==2.4.2',
        'nameko-sqlalchemy==0.0.4',
        'alembic==0.8.7',
        'marshmallow==2.9.1',
        'psycopg2==2.6.2',
        'kombu==3.0.37'
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
