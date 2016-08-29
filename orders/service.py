from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession

from orders.models import DeclarativeBase, Order, OrderDetail
from orders.schemas import OrderSchema


class OrdersService:
    name = 'orders'

    db = DatabaseSession(DeclarativeBase)
    order_schema = OrderSchema()
    event_dispatcher = EventDispatcher()

    @rpc
    def get_order(self, order_id):
        order = self.db.query(Order).get(order_id)
        return self.order_schema.dump(order).data

    @rpc
    def create_order(self, order_details):
        order = Order(
            order_details=[
                OrderDetail(
                    product_id=order_detail['product_id'],
                    price=order_detail['price'],
                    quantity=order_detail['price']
                )
                for order_detail in order_details
            ]
        )
        self.db.add(order)
        self.db.commit()

        order = self.order_schema.dump(order).data

        self.event_dispatcher('order_created', {
            'order': order,
        })

        return order

    @rpc
    def update_order(self, order):
        order_details = {
            order_details['id']: order_details
            for order_details in order['order_details']
        }

        order = self.db.query(Order).get(order['id'])

        for order_detail in order.order_details:
            order_detail.price = order_details[order_detail.id]['price']
            order_detail.quantity = order_details[order_detail.id]['quantity']

        self.db.commit()
        return self.order_schema.dump(order).data

    @rpc
    def delete_order(self, order_id):
        order = self.db.query(Order).get(order_id)
        self.db.delete(order)
        self.db.commit()
