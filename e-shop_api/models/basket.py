import sqlalchemy as sa
from sqlalchemy.orm import relationship
from models import Base


class Basket(Base):
    __tablename__ = 'basket'
    id = sa.Column(sa.Integer, primary_key=True)
    order = relationship("Order", back_populates="basket")
    users_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    users = relationship("Users", back_populates="basket")

    def __repr__(self):
        return "<order('%s','%s')>" % (self.id, self.user_id)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['name', 'login']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

