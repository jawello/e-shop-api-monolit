from aiohttp.web import Request, HTTPInternalServerError, HTTPUnauthorized, HTTPNotFound, HTTPBadRequest, HTTPNoContent
from aiohttp.web_response import Response
from aiohttp_security import authorized_userid
from sqlalchemy.exc import SQLAlchemyError

from models import Basket
from models import Users, ProductShop, ProductInBasket
from models.schemas.basket_schema import BasketSchema

from sqlalchemy.orm import sessionmaker, Session

import json

import logging

log = logging.getLogger(__name__)


async def baskets_get(request: Request) -> Response:
    login = await authorized_userid(request)
    if not login:
        return HTTPUnauthorized()

    try:
        output_params = request.rel_url.query.get('output')
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        users_id = request.query.get('users_id')
        if users_id:
            users_id = [int(x.strip()) for x in users_id.split(',')]
            baskets = session.query(Basket).join(Users).filter(Users.id.in_(users_id))
        else:
            baskets = session.query(Basket).all()

        if output_params:
            output = [x.strip() for x in output_params.split(',')]
            baskets_list = BasketSchema(many=True, only=output).dump(baskets)
        else:
            baskets_list = BasketSchema(many=True).dump(baskets)
        return Response(body=json.dumps(baskets_list), headers={'content-type': 'application/json'})
    except Exception as ex:
        log.warning(f"Endpoint: shops, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


async def baskets_id_get(request: Request) -> Response:
    try:
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        basket_id = request.match_info['id']
        if not basket_id:
            return HTTPBadRequest()

        basket = session.query(Basket).filter_by(id=basket_id).first()

        params = request.rel_url.query.get('output')
        if params:
            output = [x.strip() for x in params.split(',')]
            baskets_serialized = BasketSchema(only=output).dump(basket)
        else:
            baskets_serialized = BasketSchema().dump(basket)

        return Response(body=json.dumps(baskets_serialized), headers={'content-type': 'application/json'})
    except Exception as ex:
        log.warning(f"Endpoint: baskets/id, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


async def baskets_post(request: Request) -> Response:
    login = await authorized_userid(request)
    if not login:
        return HTTPUnauthorized()

    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session: Session = session_maker()

        if data:
            basket = BasketSchema().load(data, session=session)
            session.add(basket)
            session.commit()

            return Response(headers={'Location': f"/baskets/{basket.id}"})
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /baskets, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()


async def baskets_id_products_get(request: Request) -> Response:
    login = await authorized_userid(request)
    if not login:
        return HTTPUnauthorized()

    try:
        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session: Session = session_maker()

        basket_id = request.match_info['id']
        if not basket_id:
            return HTTPBadRequest()

        basket = session.query(Basket).filter_by(id=basket_id).first()
        pid: ProductInBasket
        result = []
        for pid in basket.product_in_basket:
            product_quantity_basket = {'product_id': pid.product_shop.product_id,
                                       'quantity': pid.quantity,
                                       'price': pid.product_shop.price}
            result.append(product_quantity_basket)

        return Response(body=json.dumps(result), headers={'content-type': 'application/json'})

    except Exception as ex:
        log.warning(f"Endpoint: /baskets/id/products, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


async def baskets_id_products_put(request: Request) -> Response:
    login = await authorized_userid(request)
    if not login:
        return HTTPUnauthorized()

    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session: Session = session_maker()

        basket_id = request.match_info['id']
        if not basket_id:
            return HTTPBadRequest()

        if not data:
            return HTTPBadRequest()

        basket = session.query(Basket).filter_by(id=basket_id).first()
        products_id = [d['product_id'] for d in data]

        products_quantity = {d['product_id']: d['quantity'] for d in data}

        products_count = session.query(ProductShop).filter(ProductShop.product_id.in_(products_id)). \
            filter(ProductShop.shop_id == basket.shop_id).count()

        if len(products_id) != products_count:
            return HTTPBadRequest()

        products_shop = session.query(ProductShop).filter(ProductShop.product_id.in_(products_id)). \
            filter(ProductShop.shop_id == basket.shop_id).all()

        for ps in products_shop:
            quantity = products_quantity[ps.product_id]
            if quantity > ps.quantity:
                return HTTPBadRequest()

            product_in_basket = ProductInBasket(product_shop=ps, basket=basket, quantity=quantity)
            session.add(product_in_basket)
            # TODO: can't update product in basket. Try to change pk of ProductInBasket to complex key: shop_id,
            #  product_id. Think about change pk for ProductShop
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return HTTPBadRequest()
        return HTTPNoContent()
    except Exception as ex:
        log.warning(f"Endpoint: /baskets/id/products, Method: put. Error:{str(ex)}")
        return HTTPInternalServerError()


def create_basket_dict(session: Session, user: Users) -> dict:
    result = {}
    baskets = session.query(Basket).filter_by(users=user).filter_by(order=None).all()
    for basket in baskets:
        result[basket.shop.id] = basket

    return result


def fill_basket(session: Session, basket_product_dict: dict, products: [], user: Users):
    result = basket_product_dict
    for product in products:
        product_shop = session.query(ProductShop).filter_by(id=product['id']).first()
        shop = session.query(ProductShop).filter_by(product_shop=product_shop).first()
        if shop.id not in result:
            result[shop.id] = Basket(users=user, shop=shop)

        basket = result[shop.id]

        product_in_basket = ProductInBasket(basket=basket, product_shop=product_shop,
                                            quantity=product['quantity'])
        session.add(product_in_basket)


async def put(request: Request) -> Response:
    try:
        login = await authorized_userid(request)
        if not login:
            return HTTPUnauthorized()
        else:
            conn = request.app['db_pool']
            session_maker = sessionmaker(bind=conn)
            session = session_maker()
            user = Users.get_user_by_login_sync(session,
                                                login=login
                                                )
        if not user:
            return HTTPNotFound()

        data = await request.json()
        if data:
            baskets_shop_dict = create_basket_dict(session, user)

            try:
                fill_basket(session, baskets_shop_dict, data["products"], user)
                session.commit()
            except Exception as ex:
                session.rollback()
                log.warning(f"Endpoint: basket, Method: put. Msg:{str(ex)}")
                return HTTPInternalServerError()

            return Response()
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: basket, Method: put. Msg:{str(ex)}")
        return HTTPInternalServerError()
