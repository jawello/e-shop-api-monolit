import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models import Base


class Order(Base):
    __tablename__ = 'order'
    id = sa.Column(sa.Integer, primary_key=True)
    basket_id = sa.Column(sa.Integer, sa.ForeignKey("basket.id"))
    basket = relationship("Basket", back_populates="order", uselist=False)
    date = sa.Column(sa.DateTime)
    status = sa.Column(sa.String, sa.ForeignKey("order_status.id"))
    order_status = relationship("OrderStatus", back_populates="order", uselist=False)

    def __repr__(self):
        return "<Order('%s','%s', '%s', '%s')>" % (self.id, self.basket_id, self.date, self.status)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['basket_id', 'date', 'status']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

