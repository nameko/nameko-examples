import pytest

from orders.models import DeclarativeBase


@pytest.fixture(scope='session')
def db_url():
    """Overriding db_url fixture from `nameko_sqlalchemy`

    `db_url` and `model_base` below are used by `db_session` fixture
    from `nameko_sqlalchemy`.

    `db_session` fixture is used for any database dependent tests.

    For more information see: https://github.com/onefinestay/nameko-sqlalchemy
    """
    return 'sqlite:///orders.sql'


@pytest.fixture(scope="session")
def model_base():
    """Overriding model_base fixture from `nameko_sqlalchemy`"""
    return DeclarativeBase
