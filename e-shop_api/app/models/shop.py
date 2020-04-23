import sqlalchemy as sa
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from models import Base


class Shop(Base):
    __tablename__ = 'shop'
    id = sa.Column('id', sa.Integer, primary_key=True)
    # TODO: add user relation
    product_shop = relationship("ProductShop", back_populates="shop")
    basket = relationship("Basket", back_populates="shop", uselist=True)
    name = sa.Column('name', sa.String, nullable=False, unique=True)
    description = sa.Column('description', sa.String)
    site = sa.Column('site', sa.String)

    def __repr__(self):
        return "<Shop('%s','%s', '%s', '%s')>" % (self.id, self.name, self.description, self.site)

    @staticmethod
    def get_shop_by_id(session, shop_id) -> 'Shop':
        result = session.query(Shop).filter_by(id=shop_id).first()
        return result


class ShopScheme(Schema):
    id = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    site = fields.URL()
    # TODO: nested field user
    # TODO: nested fields product
    # TODO: nested fields basket

