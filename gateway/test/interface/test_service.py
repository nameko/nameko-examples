from mock import call

from gateway.exceptions import OrderNotFound


class TestGetOrder(object):

    def test_can_get_order(self, gateway_service, web_session):
        # setup mock orders-service response:
        gateway_service.orders_rpc.get_order.return_value = {
            'id': 1,
            'order_details': [
                {
                    'id': 1,
                    'quantity': 2,
                    'product_id': '1',
                    'price': '200.00'
                },
                {
                    'id': 2,
                    'quantity': 1,
                    'product_id': '2',
                    'price': '400.00'
                }
            ]
        }

        # setup mock products-service response:
        gateway_service.products_rpc.list.return_value = [
            {
                'id': '1',
                'title': 'big',
                'maximum_speed': 3,
                'in_stock': 899,
                'passenger_capacity': 100
            },
            {
                'id': '2',
                'title': 'small',
                'maximum_speed': 200,
                'in_stock': 1,
                'passenger_capacity': 4
            },

        ]

        # call the gateway service to get order #1
        response = web_session.get('/orders/1')
        assert response.status_code == 200

        expected_response = {
            'id': 1,
            'order_details': [
                {
                    'id': 1,
                    'quantity': 2,
                    'product_id': '1',
                    'image': 'http://foo.com/airship/images/1.jpg',
                    'product': {
                        'id': '1',
                        'title': 'big',
                        'maximum_speed': 3,
                        'in_stock': 899,
                        'passenger_capacity': 100
                    },
                    'price': '200.00'
                },
                {
                    'id': 2,
                    'quantity': 1,
                    'product_id': '2',
                    'image': 'http://foo.com/airship/images/2.jpg',
                    'product': {
                        'id': '2',
                        'title': 'small',
                        'maximum_speed': 200,
                        'in_stock': 1,
                        'passenger_capacity': 4
                    },
                    'price': '400.00'
                }
            ]
        }
        assert expected_response == response.json()

        # check dependencies called as expected
        assert [call(1)] == gateway_service.orders_rpc.get_order.call_args_list
        assert [call()] == gateway_service.products_rpc.list.call_args_list

    def test_order_not_found(self, gateway_service, web_session):
        gateway_service.orders_rpc.get_order.side_effect = (
            OrderNotFound('missing'))

        # call the gateway service to get order #1
        response = web_session.get('/orders/1')
        assert response.status_code == 404
        payload = response.json()
        assert payload['error'] == 'ORDER_NOT_FOUND'
        assert payload['message'] == 'missing'


class TestCreateOrder(object):

    def test_can_create_order(self):
        pass

        # {
        #     'order_details': [
        #         {
        #             'product_id': '1',
        #             'price': '41',
        #             'quantity': 3
        #         }
        #     ]
        # }

        # {
        #   'id': 11
        # }
