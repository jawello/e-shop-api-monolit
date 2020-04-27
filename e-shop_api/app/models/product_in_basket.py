import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from models import ProductShop, Basket

from models import Base


class ProductInBasket(Base):
    __tablename__ = 'product_in_basket'
    id = sa.Column('id', sa.Integer, primary_key=True)

    product_shop_id = sa.Column('product_shop_id', sa.Integer, sa.ForeignKey('product_shop.id'), nullable=False)
    product_shop = relationship(ProductShop, backref=backref("product_in_basket", cascade="all, delete-orphan"))

    basket_id = sa.Column('basket_id', sa.Integer, sa.ForeignKey('basket.id'), nullable=False, unique=False)
    basket = relationship(Basket, backref=backref("product_in_basket", cascade="all, delete-orphan"))

    quantity = sa.Column('quantity', sa.Integer, default=1)

    def __repr__(self):
        return "<ProductInBasket('%s','%s', '%s', '%s')>" % (self.id,
                                                             self.basket_id,
                                                             self.product_shop_id,
                                                             self.quantity)

