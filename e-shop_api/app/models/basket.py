import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models import Base


class Basket(Base):
    __tablename__ = 'basket'
    id = sa.Column(sa.Integer, primary_key=True)
    order = relationship("Order", back_populates="basket", uselist=False)
    shop_id = sa.Column(sa.Integer, sa.ForeignKey("shop.id"))
    shop = relationship("Shop", back_populates="basket", uselist=False)
    product_in_basket = relationship("ProductInBasket", back_populates="basket")
    users_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    users = relationship("Users", back_populates="basket", uselist=False)

    def __repr__(self):
        return "<Basket('%s','%s')>" % (self.id, self.users_id)

