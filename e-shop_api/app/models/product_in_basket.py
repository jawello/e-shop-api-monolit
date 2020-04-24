import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models import Base


class ProductInBasket(Base):
    __tablename__ = 'product_in_basket'
    id = sa.Column('id', sa.Integer, primary_key=True)
    basket_id = sa.Column('basket_id', sa.Integer, sa.ForeignKey('basket.id'), nullable=False, unique=True)
    basket = relationship("Basket", back_populates="product_in_basket")
    product_shop_id = sa.Column('product_shop_id', sa.Integer, sa.ForeignKey('product_shop.id'), nullable=True)
    product_shop = relationship("ProductShop", back_populates="product_in_basket")
    quantity = sa.Column('quantity', sa.Integer, default=1)

    def __repr__(self):
        return "<ProductInBasket('%s','%s', '%s', '%s')>" % (self.id,
                                                             self.basket_id,
                                                             self.product_shop_id,
                                                             self.quantity)

