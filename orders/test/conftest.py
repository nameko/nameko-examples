import pytest

from orders.models import DeclarativeBase


@pytest.fixture(scope='session')
def db_url():
    """Overriding db_url fixture from nameko_sqlalchemy"""
    return 'sqlite:///orders.sql'


@pytest.fixture(scope="session")
def model_base():
    """Overriding model_base fixture from nameko_sqlalchemy"""
    return DeclarativeBase
