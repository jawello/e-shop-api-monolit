from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.basket import Basket


class BasketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Basket
        include_fk = True
        load_instance = True
        include_relationships = True

