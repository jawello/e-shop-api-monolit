import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from models import Base


class Shop(Base):
    __tablename__ = 'shop'
    id = sa.Column('id', sa.Integer, primary_key=True)
    products = association_proxy("product_shop", "product")
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

