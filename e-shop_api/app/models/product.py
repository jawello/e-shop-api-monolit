import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models import Base


class Product(Base):
    __tablename__ = 'product'
    id = sa.Column('id', sa.Integer, primary_key=True)
    product_shop = relationship("ProductShop", back_populates="product")
    name = sa.Column('name', sa.String, nullable=False, unique=True)
    description = sa.Column('description', sa.String)

    def __repr__(self):
        return "<Product('%s','%s', '%s')>" % (self.id, self.name, self.description)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['name', 'description']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

