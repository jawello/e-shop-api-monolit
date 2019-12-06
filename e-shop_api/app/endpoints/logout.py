from typing import List

from aiohttp.web_response import Response
from aiohttp.web import Request

from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json

from aiohttp_security import forget, authorized_userid

import logging

log = logging.getLogger(__name__)


class LoginEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/logout'
        ]

    async def post(self, request: Request) -> Response:
        try:
            user_id = await authorized_userid(request)
            if not user_id:
                return respond_with_json({"error": "Session invalid"}, status=400)
            response = respond_with_json({"status": "successful"})
            await forget(request, response)
            return response
        except Exception as ex:
            log.warning(f"Endpoint: logout, Method: post. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

