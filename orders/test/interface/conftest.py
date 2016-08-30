import pytest
from collections import namedtuple

from nameko.standalone.rpc import ServiceRpcProxy
from nameko.testing.services import replace_dependencies

from service import OrdersService


@pytest.fixture
def config(rabbit_config, db_url):
    orders_config = rabbit_config.copy()
    orders_config['DB_URIS'] = {'orders:Base': db_url}
    return orders_config


@pytest.fixture
def container(container_factory, config):
    ServiceMeta = namedtuple(
        'ServiceMeta', ['container', 'event_dispatcher']
    )
    container = container_factory(OrdersService, config)

    mocked_dependencies = replace_dependencies(
        container, 'event_dispatcher'
    )
    container.start()

    return ServiceMeta(container, mocked_dependencies)


@pytest.yield_fixture
def orders_rpc(config, container):
    with ServiceRpcProxy('orders', config) as proxy:
        yield proxy
