from aiohttp_security.abc import AbstractAuthorizationPolicy
from sqlalchemy.engine import Engine

from app.models import Users


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, db_pool: Engine):
        self.db_pool = db_pool

    async def authorized_userid(self, identity):
        user = Users.get_user_by_login(self.db_pool, identity)
        if user:
            return identity
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True

