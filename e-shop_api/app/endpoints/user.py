from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from models import Users

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)


class UserEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/user'
        ]

    @staticmethod
    async def get(request: Request) -> Response:
        try:
            login = await authorized_userid(request)
            if not login:
                return respond_with_json({"error": "Unauthorized"}, status=401)

            conn = request.app['db_pool']
            Session = sessionmaker(bind=conn)
            session = Session()

            user = Users.get_user_by_login_sync(session,
                                           login=login
                                           )
            if user:
                return respond_with_json(user.to_json())
            else:
                return respond_with_json({"error": F"No user with login {login}"}, status=404)
        except Exception as ex:
            log.warning(f"Endpoint: user, Method: get. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

    async def post(self, request: Request) -> Response:
        try:
            data = await request.json()

            conn = request.app['db_pool']
            Session = sessionmaker(bind=conn)
            session = Session()
            if data:
                user_id = Users.create_user(session,
                                            data.get('name'),
                                            data['login'],
                                            data['password'])
                return respond_with_json({"user_id": user_id})
            else:
                return respond_with_json({"error": "No parameters"}, status=400)
        except Exception as ex:
            log.warning(f"Endpoint: user, Method: get. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)
