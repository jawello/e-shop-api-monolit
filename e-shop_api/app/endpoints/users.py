from aiohttp.web import Request, HTTPUnauthorized, HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp_security import authorized_userid
from aiohttp import web
import json

from models import Users

from sqlalchemy.orm import sessionmaker

import logging

log = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get('/users/{login}')
async def users_get(request: Request) -> Response:
    try:
        login = await authorized_userid(request)
        if not login:
            return HTTPUnauthorized()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        user = Users.get_user_by_login_sync(session,
                                            login=request.match_info['login']
                                            )

        if user:
            return Response(body=json.dumps(user.to_json()))  # TODO: make with marshmallow
        else:
            return HTTPNotFound()
    except Exception as ex:
        log.warning(f"Endpoint: /users/login, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.get('/users')
async def users_get(request: Request) -> Response:
    try:
        login = await authorized_userid(request)
        if not login:
            return HTTPUnauthorized()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        users = session.query(Users)

        users_list = []
        for u in users:
            users_list.append(u.to_json())

        if users_list:
            return Response(body=json.dumps(users_list))  # TODO: make with marshmallow
        else:
            return HTTPNotFound()
    except Exception as ex:
        log.warning(f"Endpoint: /users/login, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


@routes.post('/users')
async def users_post(request: Request) -> Response:
    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()
        if data:  # TODO: make with marshmallow
            Users.create_user(session,
                              data.get('name'),
                              data['login'],
                              data['password'])
            return Response()
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /users, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()
