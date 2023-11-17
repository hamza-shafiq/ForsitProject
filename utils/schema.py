""" data serialization """

from marshmallow import fields as mf, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields
from .models import Sales, Product, Inventory, Category

class SalesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        load_instance = True
        include_relationships = True

    id = auto_field()
    amount = auto_field()
    date = auto_field()
    product_id = auto_field()




