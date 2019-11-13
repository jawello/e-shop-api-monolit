from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from models import Base
from security import generate_password_hash, check_password_hash


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    basket = relationship("Basket", back_populates="users")
    name = Column(String)
    login = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<Users('%s','%s', '%s')>" % (self.name, self.login, self.password)

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
    def get_user_by_id(session, user_id) -> 'Users':
        result = session.query(Users).filter_by(id=user_id).first()
        return result

    @staticmethod
    async def get_user_by_login(conn, login) -> 'Users':
        Session = sessionmaker(bind=conn)
        session = Session()
        result = session.query(Users).filter_by(login=login).first()
        return result

    @staticmethod
    def get_user_by_login_sync(session, login) -> 'Users':
        result = session.query(Users).filter_by(login=login).first()
        return result

    @staticmethod
    def create_user(session, name, login, password) -> int:
        user = Users(name=name, login=login, password=generate_password_hash(password))
        session.add(user)
        session.commit()
        return user.id

    @staticmethod
    def validate_user_login(session, login, password):
        user = Users.get_user_by_login_sync(session, login)

        if not user:
            return 'Invalid username'
        if not check_password_hash(password, user.password):
            return 'Invalid password'
        else:
            return None

