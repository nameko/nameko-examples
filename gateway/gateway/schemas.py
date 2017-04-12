from marshmallow import Schema, fields


class CreateOrderDetailSchema(Schema):
    product_id = fields.Str(required=True)
    price = fields.Decimal(as_string=True, required=True)
    quantity = fields.Int(required=True)


class CreateOrderSchema(Schema):
    order_details = fields.Nested(
        CreateOrderDetailSchema, many=True, required=True
    )
