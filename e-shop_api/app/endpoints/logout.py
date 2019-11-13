from typing import List

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json

from aiohttp_security import forget

import logging

log = logging.getLogger(__name__)


class LoginEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/logout'
        ]

    async def post(self, request: Request) -> Response:
        try:
            response = respond_with_json({"msg": "logout success"})
            await forget(request, response)
            return response
        except Exception as ex:
            log.warning(f"Endpoint: logout, Method: post. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

