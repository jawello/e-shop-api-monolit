from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .users import Users
from .basket import Basket
from .order import Order
