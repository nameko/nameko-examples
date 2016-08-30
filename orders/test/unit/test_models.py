from models import Order, OrderDetail


def test_can_create_order(db_session):
    order = Order()
    db_session.add(order)
    db_session.commit()
    assert order.id > 0


def test_can_create_order_detail(db_session):
    order = Order()
    order_detail_1 = OrderDetail(
        order=order,
        product_id=1,
        price=100.50,
        quantity=1
    )
    order_detail_2 = OrderDetail(
        order=order,
        product_id=2,
        price=99.50,
        quantity=2
    )

    db_session.add_all([order_detail_1, order_detail_2])
    db_session.commit()

    assert order.id > 0
    for order_detail in order.order_details:
        assert order_detail.id > 0
    assert order_detail_1.product_id == 1
    assert order_detail_1.price == 100.50
    assert order_detail_1.quantity == 1
    assert order_detail_2.product_id == 2
    assert order_detail_2.price == 99.50
    assert order_detail_2.quantity == 2
