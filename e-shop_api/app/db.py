from sqlalchemy import create_engine


async def init_db(app):
    dsn = construct_db_url(app['config']['database'])
    # pool_size = app['config']['database']['pool_size']
    pool = create_engine(dsn, pool_size=20, max_overflow=0)
    app['db_pool'] = pool
    return pool


def construct_db_url(config):
    dsn = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return dsn.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )




