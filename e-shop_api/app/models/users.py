from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.security import generate_password_hash, check_password_hash


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    basket = relationship("Basket", back_populates="users")
    order = relationship("Order", back_populates="users")
    name = Column(String)
    login = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.login, self.password)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['name', 'login']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d

    @staticmethod
    async def get_user_by_id(conn, user_id) -> 'Users':
        Session = sessionmaker(bind=conn)
        session = Session()
        result = session.query(Users).filter_by(id=user_id).first()
        return result

    @staticmethod
    async def get_user_by_login(conn, login):
        Session = sessionmaker(bind=conn)
        session = Session()
        result = session.query(Users).filter_by(login=login).first()
        return result

    @staticmethod
    async def create_user(conn, name, login, password):
        Session = sessionmaker(bind=conn)
        session = Session()
        user = Users(name=name, login=login, password=generate_password_hash(password))
        session.add(user)
        session.commit()
        return user.id

    @staticmethod
    async def validate_user_login(conn, login, password):
        user = await Users.get_user_by_login(conn, login)

        if not user:
            return 'Invalid username'
        if not check_password_hash(password, user.password):
            return 'Invalid password'
        else:
            return None
