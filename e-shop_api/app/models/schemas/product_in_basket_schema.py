from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.product_in_basket import ProductInBasket


class ProductInBasketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductInBasket
        include_fk = True
        load_instance = True
