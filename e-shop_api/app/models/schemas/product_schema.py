from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.product import Product


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True

