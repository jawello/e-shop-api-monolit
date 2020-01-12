from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from models import Basket
from models import Users
from models import ProductShop
from models import ProductInBasket
from models import Shop

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import logging

log = logging.getLogger(__name__)


class BasketEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/basket'
        ]

    @staticmethod
    def create_basket_dict(session: Session, user: Users) -> dict:
        result = {}
        baskets = session.query(Basket).filter_by(users=user).filter_by(order=None).all()
        for basket in baskets:
            result[basket.shop.id] = basket

        return result

    @staticmethod
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

            data = await request.json()
            if data:
                baskets_shop_dict = BasketEndpoint.create_basket_dict(session, user)

                try:
                    BasketEndpoint.fill_basket(session, baskets_shop_dict, data["products"], user)
                    session.commit()
                except Exception as ex:
                    session.rollback()
                    log.warning(f"Endpoint: basket, Method: put. Msg:{str(ex)}")
                    return respond_with_json({"error": "Internal Server Error"}, status=500)

                return respond_with_json({"msg": "Products add successfully"})
            else:
                return respond_with_json({"error": "No parameters"}, status=400)
        except Exception as ex:
            log.warning(f"Endpoint: basket, Method: put. Msg:{str(ex)}")
            return respond_with_json({"error": "Internal Server Error"}, status=500)

