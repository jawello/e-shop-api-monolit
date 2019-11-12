from typing import List
from datetime import datetime

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from app.models import Users


class OrderEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/orders'
        ]

    @staticmethod
    async def get(request: Request) -> Response:
        login = await authorized_userid(request)
        if not login:
            return respond_with_json({"error": "Unauthorized"}, status=401)
        else:
            db_pool = request.app['db_pool']
            user = await Users.get_user_by_login(db_pool,
                                                 login=login
                                                 )
        if not user:
            return respond_with_json({"error": F"No user with login {login}"}, status=404)

        result = []
        for basket in user.basket:
            if basket.order:
                order = {"status": basket.order.status,
                         "date": basket.order.date.isoformat()}
                products = []
                for product_in_basket in basket.product_in_basket:
                    product = {"name": product_in_basket.product_shop.product.name,
                               "quantity": product_in_basket.quantity,
                               "price": product_in_basket.product_shop.price
                               }
                    products.append(product)
                order['products'] = products

                result.append(order)
        return respond_with_json(result)
