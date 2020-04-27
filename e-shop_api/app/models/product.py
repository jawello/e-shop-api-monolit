import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy

from models import Base


class Product(Base):
    __tablename__ = 'product'
    id = sa.Column('id', sa.Integer, primary_key=True)
    shops = association_proxy("product_shop", "shop")
    name = sa.Column('name', sa.String, nullable=False, unique=True)
    description = sa.Column('description', sa.String)

    def __repr__(self):
        return "<Product('%s','%s', '%s')>" % (self.id, self.name, self.description)
