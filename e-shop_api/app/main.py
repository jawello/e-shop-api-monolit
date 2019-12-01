from aiohttp import web
from aiohttp.web import Application
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aioredis
from db_auth import DBAuthorizationPolicy
from db import init_db
from settings import load_config
from aiohttp_rest_api.loader import load_and_connect_all_endpoints_from_folder
import logging

log = logging.getLogger(__name__)


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((
        app['config']['redis']['REDIS_HOST'],
        app['config']['redis']['REDIS_PORT']
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


async def init_app(config)-> Application:
    app = web.Application()

    app['config'] = config

    load_and_connect_all_endpoints_from_folder(
        path='endpoints',
        app=app,
        version_prefix='v1'
    )

    db_pool = await init_db(app)

    redis_pool = await setup_redis(app)
    setup_session(app, RedisStorage(redis_pool))

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db_pool)
    )

    log.debug(app['config'])

    return app


def main(config_path):
    config = load_config(config_path)
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(config)
    app_config = config.get('app', None)
    if not app_config:
        web.run_app(app, port=app_config.get('port', 8080))
    else:
        web.run_app(app, port=8080)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
