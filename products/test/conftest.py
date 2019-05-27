import pytest
import redis

from nameko import config
from products.dependencies import REDIS_URI_KEY


@pytest.fixture
def test_config(rabbit_config):
    with config.patch(
        {REDIS_URI_KEY: 'redis://localhost:6379/11'}
    ):
        yield


@pytest.yield_fixture
def redis_client(test_config):
    client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))
    yield client
    client.flushdb()


@pytest.fixture
def product():
    return {
        'id': 'LZ127',
        'title': 'LZ 127',
        'passenger_capacity': 72,
        'maximum_speed': 130,
        'in_stock': 11,
    }


@pytest.fixture
def create_product(redis_client, product):
    def create(**overrides):
        new_product = product.copy()
        new_product.update(**overrides)
        redis_client.hmset(
            'products:{}'.format(new_product['id']),
            new_product)
        return new_product
    return create


@pytest.fixture
def products(create_product):
    return [
        create_product(
            id='LZ127',
            title='LZ 127 Graf Zeppelin',
            passenger_capacity=20,
            maximum_speed=128,
            in_stock=10,
        ),
        create_product(
            id='LZ129',
            title='LZ 129 Hindenburg',
            passenger_capacity=50,
            maximum_speed=135,
            in_stock=11,
        ),
        create_product(
            id='LZ130',
            title='LZ 130 Graf Zeppelin II',
            passenger_capacity=72,
            maximum_speed=135,
            in_stock=12,
        ),
    ]
