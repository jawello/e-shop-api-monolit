from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.shop import Shop


class ShopSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shop
        include_fk = True
        load_instance = True

