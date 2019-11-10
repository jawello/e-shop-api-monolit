from typing import List

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from models.users import Users


class UserEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/user'
        ]

    async def get(self, request: Request) -> Response:
        login = await authorized_userid(request)
        if not login:
            return respond_with_json({"error": "Unauthorized"}, status=401)
        else:
            user = await Users.get_user_by_login(request.app['db_pool'],
                                                 login=login
                                                 )
            if user:
                return respond_with_json(user.to_json())
            else:
                return respond_with_json({"error": F"No user with login {login}"}, status=404)

    async def post(self, request: Request) -> Response:
        try:
            data = await request.json()
            if data:
                user_id = await Users.create_user(request.app['db_pool'],
                                                  data.get('name'),
                                                  data['login'],
                                                  data['password'])
                return respond_with_json({"user_id": user_id})
            else:
                return respond_with_json({"error": "No parameters"}, status=400)
        except Exception as ex:
            return respond_with_json({"error": str(ex)}, status=400)
