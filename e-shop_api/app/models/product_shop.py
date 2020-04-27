import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from models import Base


class ProductShop(Base):
    __tablename__ = 'product_shop'
    id = sa.Column('id', sa.Integer, primary_key=True)

    shop_id = sa.Column('shop_id', sa.Integer, sa.ForeignKey('shop.id'), nullable=False)
    shop = relationship("Shop", backref=backref("product_shop", cascade="all, delete-orphan"))

    quantity = sa.Column('quantity', sa.Integer)
    price = sa.Column('price', sa.Float)

    product_id = sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), nullable=False)
    product = relationship("Product",
                           backref=backref("product_shop",
                                           cascade="all, delete-orphan"
                                           )
                           )

    def __repr__(self):
        return "<ProductShop('%s','%s', '%s', '%s', '%s')>" % (self.id,
                                                               self.product_id,
                                                               self.shop_id,
                                                               self.price,
                                                               self.quantity)
