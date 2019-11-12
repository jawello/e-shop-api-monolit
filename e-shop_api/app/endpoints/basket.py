from typing import List

from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
from aiohttp_security import authorized_userid

from app.models import Basket
from app.models import Users
from app.models import ProductShop
from app.models import ProductInBasket

from sqlalchemy.orm import sessionmaker


class BasketEndpoint(AioHTTPRestEndpoint):
    def connected_routes(self) -> List[str]:
        return [
            '/basket'
        ]

    @staticmethod
    async def put(request: Request) -> Response:
        try:
            login = await authorized_userid(request)
            if not login:
                return respond_with_json({"error": "Unauthorized"}, status=401)
            else:
                conn = request.app['db_pool']
                user = await Users.get_user_by_login(conn,
                                                     login=login
                                                     )
            if not user:
                return respond_with_json({"error": F"No user with login {login}"}, status=404)

            data = await request.json()
            if data:
                Session = sessionmaker(bind=conn)
                session = Session()

                basket = session.query(Basket).filter_by(users=user).first()
                if not basket:
                    basket = Basket(users=user)

                try:
                    for product in data["products"]:
                        product_shop = session.query(ProductShop).filter_by(id=product['id']).first()
                        product_in_basket = ProductInBasket(basket=basket, product_shop=product_shop,
                                                            quantity=product['quantity'])
                        session.add(product_in_basket)
                    session.commit()
                except Exception as ex:
                    session.rollback()
                    return respond_with_json({"error": str(ex)}, status=400)

                return respond_with_json({"msg": "Products add successfully"})
            else:
                return respond_with_json({"error": "No parameters"}, status=400)
        except Exception as ex:
            return respond_with_json({"error": str(ex)}, status=400)

