from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import remember, authorized_userid

from models import Users

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)


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
                conn = request.app['db_pool']
                Session = sessionmaker(bind=conn)
                session = Session()
                error = Users.validate_user_login(session, data['login'], data['password'])
                if not error:
                    user = Users.get_user_by_login_sync(session,
                                                        login=data['login']
                                                        )
                    response = respond_with_json({"status": "successful"})
                    await remember(request, response, user.login)
                    return response
                else:
                    return respond_with_json({"status": "unsuccessful", "error": error}, status=401)
            else:
                return respond_with_json({"error": "Bad parameters"})
        except Exception as ex:
            log.warning(f"Endpoint: login, Method: post. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)
