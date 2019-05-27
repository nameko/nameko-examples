import pytest
from mock import Mock

from nameko import config
from products.dependencies import Storage


@pytest.fixture
def storage(test_config):
    provider = Storage()
    provider.container = Mock(config=config)
    provider.setup()
    return provider.get_dependency({})


def test_get_fails_on_not_found(storage):
    with pytest.raises(storage.NotFound) as exc:
        storage.get(2)
    assert 'Product ID 2 does not exist' == exc.value.args[0]


def test_get(storage, products):
    product = storage.get('LZ129')
    assert 'LZ129' == product['id']
    assert 'LZ 129 Hindenburg' == product['title']
    assert 135 == product['maximum_speed']
    assert 50 == product['passenger_capacity']
    assert 11 == product['in_stock']


def test_list(storage, products):
    listed_products = storage.list()
    assert (
        products == sorted(list(listed_products), key=lambda x: x['id']))


def test_create(product, redis_client, storage):

    storage.create(product)

    stored_product = redis_client.hgetall('products:LZ127')

    assert product['id'] == stored_product[b'id'].decode('utf-8')
    assert product['title'] == stored_product[b'title'].decode('utf-8')
    assert product['maximum_speed'] == int(stored_product[b'maximum_speed'])
    assert product['passenger_capacity'] == (
        int(stored_product[b'passenger_capacity']))
    assert product['in_stock'] == int(stored_product[b'in_stock'])


def test_decrement_stock(storage, create_product, redis_client):
    create_product(id=1, title='LZ 127', in_stock=10)
    create_product(id=2, title='LZ 129', in_stock=11)
    create_product(id=3, title='LZ 130', in_stock=12)

    in_stock = storage.decrement_stock(2, 4)

    assert 7 == in_stock
    product_one, product_two, product_three = [
        redis_client.hgetall('products:{}'.format(id_))
        for id_ in (1, 2, 3)]
    assert b'10' == product_one[b'in_stock']
    assert b'7' == product_two[b'in_stock']
    assert b'12' == product_three[b'in_stock']
