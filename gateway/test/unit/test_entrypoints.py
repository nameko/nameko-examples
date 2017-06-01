import json
import pytest
from marshmallow import ValidationError

from gateway.entrypoints import HttpEntrypoint
from gateway.exceptions import ProductNotFound, OrderNotFound


class TestHttpEntrypoint(object):

    @pytest.mark.parametrize(
        ('exc', 'expected_error', 'expected_status_code',
            'expected_message'), [
            (ValueError('unexpected'), 'UNEXPECTED_ERROR', 500, 'unexpected'),
            (ValidationError('v1'), 'VALIDATION_ERROR', 400, 'v1'),
            (ProductNotFound('p1'), 'PRODUCT_NOT_FOUND', 404, 'p1'),
            (OrderNotFound('o1'), 'ORDER_NOT_FOUND', 404, 'o1'),
            (TypeError('t1'), 'BAD_REQUEST', 400, 't1'),
        ]
    )
    def test_error_handling(
        self, exc, expected_error, expected_status_code, expected_message
    ):
        entrypoint = HttpEntrypoint('GET', 'url')
        entrypoint.expected_exceptions = (
            ValidationError,
            ProductNotFound,
            OrderNotFound,
            TypeError,
        )

        response = entrypoint.response_from_exception(exc)
        response_data = json.loads(response.data.decode())

        assert response.mimetype == 'application/json'
        assert response.status_code == expected_status_code
        assert response_data['error'] == expected_error
        assert response_data['message'] == expected_message
