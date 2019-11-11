import sqlalchemy as sa
from sqlalchemy.orm import relationship
from models import Base


class Order(Base):
    __tablename__ = 'order'
    id = sa.Column(sa.Integer, primary_key=True)
    users_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    users = relationship("Users", back_populates="order")
    basket_id = sa.Column(sa.Integer, sa.ForeignKey("basket.id"))
    basket = relationship("Basket", back_populates="order")
    date = sa.Column(sa.DateTime)
    #status = sa.Column(sa.String)
    #order_status = relationship("OrderStatus", back_populates="order")

    def __repr__(self):
        return "<order('%s','%s', '%s', '%s', '%s')>" % (self.id, self.user_id, self.basket_id, self.date, self.status)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['basket', 'users', 'date']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

