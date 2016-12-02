import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug import Response


class OrderNotFound(Exception):
    pass


class Gateway(object):
    """
    Service acts as a gateway to allow access to our other service over http.
    """
    name = 'gateway'

    # TODO - config dependency
    # TODO - schemas?

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
        Get the order details for order given by `order_id`.
        Also asynchronously collects product details for the order from the
        product service.
        """
        order = self.orders_rpc.get_order(order_id)
        if not order:
            # TODO maybe should make sure we return a 404?
            raise OrderNotFound('Order id {}'.format(order_id))

        # make async calls to products service.
        product_results = [
            self.products_rpc.get_product.call_async(product_id)
            for product_id in order['product_ids']
        ]

        # modify the order dict to include product details
        order['products'] = [result.result() for result in product_results]

        # TODO - prepend configured domain name to product images.

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
