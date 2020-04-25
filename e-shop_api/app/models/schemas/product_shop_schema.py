from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.product_shop import ProductShop


class ProductShopSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductShop
        include_fk = True
        load_instance = True

