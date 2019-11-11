import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models import Base


class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = sa.Column('id', sa.String, primary_key=True)
    order = relationship("Order", back_populates="order_status")

    def __repr__(self):
        return "<order_status('%s')>" % (self.id)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['name', 'description']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

