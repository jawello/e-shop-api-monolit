from aiohttp.web import Request, HTTPInternalServerError, HTTPBadRequest, HTTPConflict
from aiohttp.web_response import Response
from aiohttp import web
import json

from models.product import Product
from models.schemas.product_schema import ProductSchema
from models.product_shop import ProductShop
from models.schemas.product_shop_schema import ProductShopSchema

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

        output_params = request.rel_url.query.get('output')
        if output_params:
            output = [x.strip() for x in output_params.split(',')]
            products_serialized = ProductSchema(many=True, only=output).dump(result)
        else:
            products_serialized = ProductSchema(many=True).dump(result)

        return Response(body=json.dumps(products_serialized), headers={'content-type': 'application/json'})
    except Exception as ex:
        log.warning(f"Endpoint: products, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.get("/products/{id}")
async def products_id_get(request: Request) -> Response:
    try:
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        product_id = request.match_info['id']
        if not product_id:
            return HTTPBadRequest()

        result = session.query(Product).filter_by(id=product_id).first()

        params = request.rel_url.query.get('output')
        if params:
            output = [x.strip() for x in params.split(',')]
            products_serialized = ProductSchema(only=output).dump(result)
        else:
            products_serialized = ProductSchema().dump(result)

        return Response(body=json.dumps(products_serialized), headers={'content-type': 'application/json'})
    except Exception as ex:
        log.warning(f"Endpoint: products/id, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.post('/products')
async def products_post(request: Request) -> Response:
    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        if data:
            product_shop_data = data.pop('product_shop', None)
            product = ProductSchema().load(data, session=session)
            session.add(product)
            session.commit()

            if product_shop_data:
                product_shop_data['product_id'] = product.id
                product_shop = ProductShopSchema().load(product_shop_data, session=session)
                session.add(product_shop)
                session.commit()
            return Response(headers={'location': f"/products/{product.id}"})
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /products, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.post('/products/{id}/shops')
async def products_shop_post(request: Request) -> Response:
    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        product_id = request.match_info['id']
        if not product_id:
            return HTTPBadRequest()

        product = session.query(Product).filter_by(id=product_id).first()

        if data:
            product_shop_data = data
            product_shop_data['product_id'] = product.id

            query = session.query(ProductShop).filter_by(shop_id=product_shop_data["shop_id"], product_id=product.id)
            if session.query(query.exists()).scalar():
                return HTTPConflict()

            product_shop = ProductShopSchema().load(product_shop_data, session=session)
            session.add(product_shop)
            session.commit()
            return Response(headers={'Location': f"/products/{product.id}"})
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /products, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()

