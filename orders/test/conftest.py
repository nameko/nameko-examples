import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orders.models import Base


@pytest.yield_fixture(scope="module")
def connection():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    connection = engine.connect()
    Base.metadata.bind = engine
    yield connection
    Base.metadata.drop_all()
    engine.dispose()


@pytest.yield_fixture
def session(connection):
    session = sessionmaker(bind=connection)
    db_session = session()

    yield db_session

    db_session.rollback()

    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())

    db_session.commit()
    db_session.close()
