from marshmallow import Schema, fields


class OrderDetailSchema(Schema):
    id = fields.Int()
    product_id = fields.Int()
    price = fields.Decimal(as_string=True)
    quantity = fields.Int()


class OrderSchema(Schema):
    id = fields.Int()
    order_details = fields.Nested(OrderDetailSchema, many=True)
