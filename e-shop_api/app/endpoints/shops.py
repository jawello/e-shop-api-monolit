from aiohttp.web import Request, HTTPInternalServerError, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp import web
import json

from models.shop import Shop, ShopScheme

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get("/shops")
async def shops_get(request: Request) -> Response:
    try:
        params = request.rel_url.query.get('output')
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        shops = session.query(Shop).all()
        if params:
            output = [x.strip() for x in params.split(',')]
            shops_list = ShopScheme(many=True, only=output).dump(shops)
        else:
            shops_list = ShopScheme(many=True).dump(shops)
        return Response(body=json.dumps(shops_list))
    except Exception as ex:
        log.warning(f"Endpoint: shops, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.get("/shops/{id}")
async def shops_id_get(request: Request) -> Response:
    try:
        shop_id = request.match_info['id']
        if not shop_id:
            return HTTPBadRequest()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        shops = Shop.get_shop_by_id(session, shop_id)
        params = request.rel_url.query.get('output')
        if params:
            output = [x.strip() for x in params.split(',')]
            shops_serialized = ShopScheme(only=output).dump(shops)
        else:
            shops_serialized = ShopScheme().dump(shops)
        return Response(body=json.dumps(shops_serialized))
    except Exception as ex:
        log.warning(f"Endpoint: shops, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.post('/shops')
async def shops_post(request: Request) -> Response:
    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()
        if data:
            shop_data = ShopScheme().load(data)
            shop = Shop(**shop_data)
            session.add(shop)
            session.commit()
            return Response(headers={'location': f"/shops/{shop.id}"})
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /users, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()
