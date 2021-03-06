import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models import Base


class ProductShop(Base):
    __tablename__ = 'product_shop'
    id = sa.Column('id', sa.Integer, primary_key=True)
    product_in_basket = relationship("ProductInBasket", back_populates="product_shop")

    product_id = sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="product_shop", uselist=False)

    shop_id = sa.Column('shop_id', sa.Integer, sa.ForeignKey('shop.id'), nullable=False)
    shop = relationship("Shop", back_populates="product_shop", uselist=False)

    price = sa.Column('price', sa.Float)

    quantity = sa.Column('quantity', sa.Integer)

    def __repr__(self):
        return "<ProductShop('%s','%s', '%s', '%s', '%s')>" % (self.id,
                                                               self.product_id,
                                                               self.shop_id,
                                                               self.price,
                                                               self.quantity)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'product_id', 'shop_id', 'price', 'quantity']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d
