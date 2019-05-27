""" Interface Testing is performed to evaluate whether service's internal
    components act as expected.

    These tests (unlike unit tests) should use real entrypoints to trigger
    service's functionality.

    Interface tests will often use real dependencies when appropriate.

    When to use mocked vs real dependencies:

    Use mock for dependencies that deal with external services which are not a
    part of service's bounded context.

    User real dependencies for testing interaction with internal systems that
    you have a full control of like databases and file systems.

    Dependencies themselves should all have their own
    set of unit and interface tests.
"""

import pytest
from collections import namedtuple

from nameko import config
from nameko.standalone.rpc import ServiceRpcProxy
from nameko.testing.services import replace_dependencies

from orders.service import OrdersService


@pytest.fixture
def test_config(rabbit_config, db_url):
    with config.patch({'DB_URIS': {'orders:Base': db_url}}):
        yield


@pytest.fixture
def create_service_meta(container_factory, test_config):
    """ Returns a convenience method for creating service test instance

    `container_factory` is a Nameko's test fixture
    for creating service container
    """
    def create(*dependencies, **dependency_map):
        """ Create service instance with specified dependencies mocked

        Dependencies named in *dependencies will be replaced with a
        `MockDependencyProvider`, which injects a `MagicMock` instead of the
        dependency.

        Alternatively, you may use `dependency_map` keyword arguments
        to name a dependency and provide the replacement value that
        the `MockDependencyProvider` should inject.

        For more information read:
        https://github.com/onefinestay/nameko/blob/master/nameko/testing/services.py#L325
        """
        dependency_names = list(dependencies) + list(dependency_map.keys())

        ServiceMeta = namedtuple(
            'ServiceMeta', ['container'] + dependency_names
        )
        container = container_factory(OrdersService)

        mocked_dependencies = replace_dependencies(
            container, *dependencies, **dependency_map
        )
        if len(dependency_names) == 1:
            mocked_dependencies = (mocked_dependencies, )

        container.start()

        return ServiceMeta(container, *mocked_dependencies, **dependency_map)

    return create


@pytest.fixture
def orders_service(create_service_meta):
    """ Orders service test instance with `event_dispatcher`
    dependency mocked """
    return create_service_meta('event_dispatcher')


@pytest.fixture
def orders_rpc(orders_service):
    """ Fixture used for triggering real RPC entrypoints on Orders service """
    with ServiceRpcProxy('orders') as proxy:
        yield proxy
