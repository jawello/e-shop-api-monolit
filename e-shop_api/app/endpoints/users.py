from aiohttp.web import Request, HTTPUnauthorized, HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp_security import authorized_userid
import json

from models import Users
from models.schemas.users_schema import UsersSchema

from sqlalchemy.orm import sessionmaker, Session

import logging

log = logging.getLogger(__name__)


async def users_get(request: Request) -> Response:
    try:
        login = await authorized_userid(request)
        if not login:
            return HTTPUnauthorized()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()

        users = session.query(Users).all()

        params = request.rel_url.query.get('output')
        if params:
            output = [x.strip() for x in params.split(',')]
            users_serialized = UsersSchema(only=output, many=True).dump(users)
        else:
            users_serialized = UsersSchema(many=True).dump(users)

        return Response(body=json.dumps(users_serialized),
                        headers={'content-type': 'application/json'})

    except Exception as ex:
        log.warning(f"Endpoint: /users, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


async def users_login_get(request: Request) -> Response:
    try:
        login = await authorized_userid(request)
        if not login:
            return HTTPUnauthorized()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session: Session = session_maker()

        user = session.query(Users).filter_by(login=request.match_info['login']).first()

        if not user:
            return HTTPNotFound()

        params = request.rel_url.query.get('output')
        if params:
            output = [x.strip() for x in params.split(',')]
            user_serialized = UsersSchema(only=output).dump(user)
        else:
            user_serialized = UsersSchema().dump(user)

        return Response(body=json.dumps(user_serialized),
                        headers={'content-type': 'application/json'})
    except Exception as ex:
        log.warning(f"Endpoint: /users/login, Method: get. Error:{str(ex)}")
        return HTTPInternalServerError()


async def users_post(request: Request) -> Response:
    try:
        data = await request.json()

        conn = request.app['db_pool']
        session_maker = sessionmaker(bind=conn)
        session = session_maker()
        if data:
            user = UsersSchema().load(data, session=session)
            session.add(user)
            session.commit()
            return Response(headers={'Location': f"/users/{user.id}"})
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /users, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()
