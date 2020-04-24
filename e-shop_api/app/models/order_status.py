import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models import Base


class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = sa.Column('id', sa.String, primary_key=True)
    order = relationship("Order", back_populates="order_status")

    def __repr__(self):
        return "<OrderStatus('%s')>" % self.id

