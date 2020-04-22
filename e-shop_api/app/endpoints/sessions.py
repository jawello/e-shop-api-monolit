from aiohttp.web import Request, HTTPUnauthorized, HTTPInternalServerError, HTTPAccepted, HTTPBadRequest, HTTPNoContent
from aiohttp.web_response import Response
from aiohttp_security import remember, authorized_userid, forget
from models import Users
from sqlalchemy.orm import sessionmaker
import logging

log = logging.getLogger(__name__)


async def sessions_post(request: Request) -> Response:
    try:
        data = await request.json()
        if data:
            conn = request.app['db_pool']
            session_maker = sessionmaker(bind=conn)
            session = session_maker()
            error = Users.validate_user_login(session, data['login'], data['password'])
            user = Users.get_user_by_login_sync(session,
                                                login=data['login']
                                                )
            user_id = await authorized_userid(request)
            if not error:
                response = HTTPAccepted()
                await remember(request, response, user.login)
                return response
            else:
                response = HTTPUnauthorized()
                if user_id:
                    await forget(request, response)
                return response
        else:
            return HTTPBadRequest()
    except Exception as ex:
        log.warning(f"Endpoint: /sessions/new, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()


async def sessions_delete(request: Request) -> Response:
    try:
        user_id = await authorized_userid(request)
        if not user_id:
            return HTTPUnauthorized()
        await forget(request, HTTPNoContent())
        return HTTPNoContent()
    except Exception as ex:
        log.warning(f"Endpoint: /sessions, Method: post. Error:{str(ex)}")
        return HTTPInternalServerError()
