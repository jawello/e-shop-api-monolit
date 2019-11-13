from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from models import Shop

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)


class ShopCatalogEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/shop_catalog'
        ]

    @staticmethod
    async def get(request: Request) -> Response:
        try:
            login = await authorized_userid(request)
            if not login:
                return respond_with_json({"error": "Unauthorized"}, status=401)

            shop_id = request.query.get('id')

            if not shop_id:
                return respond_with_json({"error": "No shop id in request"}, status=400)

            conn = request.app['db_pool']
            Session = sessionmaker(bind=conn)
            session = Session()

            result = []

            shop = Shop.get_shop_by_id(session, shop_id)
            for product_shop in shop.product_shop:
                result.append({"name": product_shop.product.name, "description": product_shop.product.description,
                               "price": product_shop.price, "quantity": product_shop.quantity})

            return respond_with_json({"catalog": result})
        except Exception as ex:
            log.warning(f"Endpoint: shop_catalog, Method: get. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

