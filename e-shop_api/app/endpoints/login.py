from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import remember, authorized_userid, forget

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
        try:
            data = await request.json()
            if data:
                conn = request.app['db_pool']
                Session = sessionmaker(bind=conn)
                session = Session()
                error = Users.validate_user_login(session, data['login'], data['password'])
                user = Users.get_user_by_login_sync(session,
                                                    login=data['login']
                                                    )
                user_id = await authorized_userid(request)
                if not error:
                    response = respond_with_json({"status": "successful"})
                    if user_id:
                        return response
                    else:
                        await remember(request, response, user.login)
                        return response
                else:
                    response = respond_with_json({"status": "unsuccessful", "error": error}, status=401)
                    if user_id:
                        await forget(request, response)
                    return response
            else:
                return respond_with_json({"error": "Bad parameters"}, status=400)
        except Exception as ex:
            log.warning(f"Endpoint: login, Method: post. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)
