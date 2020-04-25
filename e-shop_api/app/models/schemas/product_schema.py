from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models.product import Product
from models.schemas.product_shop_schema import ProductShopSchema


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

    product_shop = Nested(ProductShopSchema, many=True, exclude=("product_id", "id"))

