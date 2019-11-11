import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models import Base


class Shop(Base):
    __tablename__ = 'shop'
    id = sa.Column('id', sa.Integer, primary_key=True)
    product_shop = relationship("ProductShop", back_populates="shop")
    name = sa.Column('name', sa.String, nullable=False, unique=True)
    description = sa.Column('description', sa.String)
    site = sa.Column('site', sa.String)

    def __repr__(self):
        return "<shop('%s','%s', '%s', '%s')>" % (self.id, self.name, self.description, self.site)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['name', 'description', 'site']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

