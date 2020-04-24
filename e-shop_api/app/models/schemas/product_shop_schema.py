from marshmallow import Schema
from models.product_shop import ProductShop


class ProductShopSchema(Schema):
    class Meta:
        model = ProductShop
        include_fk = True
        load_instance = True
