from typing import List

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json

from aiohttp_security import remember, forget, authorized_userid


class LoginEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/logout'
        ]

    async def post(self, request: Request) -> Response:
        response = respond_with_json({"msg": "logout success"})
        await forget(request, response)
        return response

