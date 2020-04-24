from aiohttp.web import Request, HTTPInternalServerError
from aiohttp.web_response import Response
from aiohttp import web
import json

from models.product import Product
from models.schemas.product_schema import ProductSchema
from models.product_shop import ProductShop

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get("/products")
async def products_get(request: Request) -> Response:
    try:
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        shops_id = request.query.get('shops_id')
        if shops_id:
            shops_id = [int(x.strip()) for x in shops_id.split(',')]
            result = session.query(Product).join(ProductShop).filter(ProductShop.shop_id.in_(shops_id))
        else:
            result = session.query(Product).all()

        products_result = ProductSchema(many=True).dump(result)

        return Response(body=json.dumps(products_result))
    except Exception as ex:
        log.warning(f"Endpoint: shop_catalog, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()