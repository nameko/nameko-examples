import json
from nameko.exceptions import RemoteError
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug import Response


class OrderNotFound(Exception):
    pass


class Gateway(object):

    name = 'gateway'

    """
    Service acts as a gateway and allows access to our other service over http.

    """
    orders_rpc = RpcProxy('orders')
    products_rpc = RpcProxy('products')

    @http('GET', '/orders')
    def list_orders(self, request):
        """
        List all orders in the system.
        """
        orders = self.orders_rpc.list_orders()

        return Response(json.dumps(orders), mimetype='application/json')

    @http("GET", "/orders/<int:order_id>", expected_exceptions=OrderNotFound)
    def get_order(self, request, order_id):
        """
        Get the order details for order given by `order_id`
        """
        try:
            order = self.orders_rpc.get_order(order_id)
        except RemoteError:
            # should we show error handling? (as this isn't very good!)
            raise OrderNotFound('Order id {}'.format(order_id))

        return Response(json.dumps(order), mimetype='application/json')

    @http("POST", "/orders")
    def create_order(self, request):
        """
        Create a new order - order data is posted as json
        """
        order_data = json.loads(request.get_data(as_text=True))

        # some data validation would be needed.

        order_result = self.rpc.orders.create_order(order_data)

        return Response(json.dumps(order_result), mimetype='application/json')
