from datetime import datetime
from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from models import Users
from models import Basket
from models import Order

from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

import logging

log = logging.getLogger(__name__)


class OrderEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/order'
        ]

    @staticmethod
    async def get(request: Request) -> Response:
        try:
            login = await authorized_userid(request)
            if not login:
                return respond_with_json({"error": "Unauthorized"}, status=401)

            conn = request.app['db_pool']
            Session = sessionmaker(bind=conn)
            session = Session()
            user = Users.get_user_by_login_sync(session,
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
        except Exception as ex:
            log.warning(f"Endpoint: order, Method: get. Error:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

    @staticmethod
    async def put(request: Request) -> Response:
        try:
            login = await authorized_userid(request)
            if not login:
                return respond_with_json({"error": "Unauthorized"}, status=401)
            else:
                conn = request.app['db_pool']
                Session = sessionmaker(bind=conn)
                session = Session()
                user = Users.get_user_by_login_sync(session,
                                                    login=login
                                                    )
            if not user:
                return respond_with_json({"error": F"No user with login {login}"}, status=404)

            basket = session.query(Basket).filter_by(users=user).filter_by(order=None).first()
            if not basket:
                return respond_with_json({"error": "Basket is empty"}, status=400)

            try:
                order = Order(basket=basket, date=datetime.now(), status="awaiting payment")
                basket.order = order

                session.add(order)
                session.add(basket)
                session.commit()
            except Exception as ex:
                session.rollback()
                log.warning(f"Endpoint: order, Method: put. Msg:{str(ex)}")
                return respond_with_json({"error": "Internal Server Error"}, status=500)

            return respond_with_json({"msg": "Order create successfully", "order_status": "awaiting payment"})
        except Exception as ex:
            log.warning(f"Endpoint: order, Method: put. Msg:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

