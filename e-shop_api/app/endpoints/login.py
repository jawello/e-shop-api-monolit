from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import remember, authorized_userid

from app.models import Users


class LoginEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/login'
        ]

    async def post(self, request: Request) -> Response:
        user_id = await authorized_userid(request)
        if user_id:
            return respond_with_json({"msg": "login success"})

        try:
            data = await request.json()
            if data:
                error = await Users.validate_user_login(request.app['db_pool'], data['login'], data['password'])
                if not error:
                    user = await Users.get_user_by_login(request.app['db_pool'],
                                                         login=data['login']
                                                         )
                    response = respond_with_json({"msg": "login success"})
                    await remember(request, response, user.login)
                    return response
                else:
                    return respond_with_json({"error": error}, status=401)
            else:
                return respond_with_json({"error": "No parameters"})
        except Exception as ex:
            return respond_with_json({"error": str(ex)})
