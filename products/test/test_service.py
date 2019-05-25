from marshmallow.exceptions import ValidationError
from nameko.testing.services import entrypoint_hook
from nameko.standalone.events import event_dispatcher
from nameko.testing.services import entrypoint_waiter
import pytest

from products.dependencies import NotFound
from products.service import ProductsService


@pytest.fixture
def service_container(test_config, container_factory):
    container = container_factory(ProductsService)
    container.start()
    return container


def test_get_product(create_product, service_container):

    stored_product = create_product()

    with entrypoint_hook(service_container, 'get') as get:
        loaded_product = get(stored_product['id'])

    assert stored_product == loaded_product


def test_get_product_fails_on_not_found(service_container):

    with pytest.raises(NotFound):
        with entrypoint_hook(service_container, 'get') as get:
            get(111)


def test_list_products(products, service_container):

    with entrypoint_hook(service_container, 'list') as list_:
        listed_products = list_()

    assert products == sorted(listed_products, key=lambda p: p['id'])


def test_list_productis_when_empty(service_container):

    with entrypoint_hook(service_container, 'list') as list_:
        listed_products = list_()

    assert [] == listed_products


def test_create_product(product, redis_client, service_container):

    with entrypoint_hook(service_container, 'create') as create:
        create(product)

    stored_product = redis_client.hgetall('products:LZ127')

    assert product['id'] == stored_product[b'id'].decode('utf-8')
    assert product['title'] == stored_product[b'title'].decode('utf-8')
    assert product['maximum_speed'] == int(stored_product[b'maximum_speed'])
    assert product['passenger_capacity'] == (
        int(stored_product[b'passenger_capacity']))
    assert product['in_stock'] == int(stored_product[b'in_stock'])


@pytest.mark.parametrize('product_overrides, expected_errors', [
    ({'id': 111}, {'id': ['Not a valid string.']}),
    (
        {'passenger_capacity': 'not-an-integer'},
        {'passenger_capacity': ['Not a valid integer.']}
    ),
    (
        {'maximum_speed': 'not-an-integer'},
        {'maximum_speed': ['Not a valid integer.']}
    ),
    (
        {'in_stock': 'not-an-integer'},
        {'in_stock': ['Not a valid integer.']}
    ),
])
def test_create_product_validation_error(
    product_overrides, expected_errors, product, redis_client,
    service_container
):

    product.update(product_overrides)

    with pytest.raises(ValidationError) as exc_info:
        with entrypoint_hook(service_container, 'create') as create:
            create(product)

    assert expected_errors == exc_info.value.args[0]


@pytest.mark.parametrize('field', [
    'id', 'title', 'passenger_capacity', 'maximum_speed', 'in_stock'])
def test_create_product_validation_error_on_required_fields(
    field, product, redis_client, service_container
):

    product.pop(field)

    with pytest.raises(ValidationError) as exc_info:
        with entrypoint_hook(service_container, 'create') as create:
            create(product)

    assert (
        {field: ['Missing data for required field.']} ==
        exc_info.value.args[0])


@pytest.mark.parametrize('field', [
    'id', 'title', 'passenger_capacity', 'maximum_speed', 'in_stock'])
def test_create_product_validation_error_on_non_nullable_fields(
    field, product, redis_client, service_container
):

    product[field] = None

    with pytest.raises(ValidationError) as exc_info:
        with entrypoint_hook(service_container, 'create') as create:
            create(product)

    assert (
        {field: ['Field may not be null.']} ==
        exc_info.value.args[0])


def test_handle_order_created(
    test_config, products, redis_client, service_container
):

    dispatch = event_dispatcher()

    payload = {
        'order': {
            'order_details': [
                {'product_id': 'LZ129', 'quantity': 2},
                {'product_id': 'LZ127', 'quantity': 4},
            ]
        }
    }

    with entrypoint_waiter(service_container, 'handle_order_created'):
        dispatch('orders', 'order_created', payload)

    product_one, product_two, product_three = [
        redis_client.hgetall('products:{}'.format(id_))
        for id_ in ('LZ127', 'LZ129', 'LZ130')]
    assert b'6' == product_one[b'in_stock']
    assert b'9' == product_two[b'in_stock']
    assert b'12' == product_three[b'in_stock']
