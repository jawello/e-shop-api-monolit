from endpoints.sessions import sessions_post, sessions_delete
from endpoints.users import users_get, users_post
from endpoints.shops import shops_get, shops_id_get, shops_post, shops_id_products_get
from endpoints.products import products_get, products_id_get, products_post, products_shops_get, products_shops_post
from endpoints.basket import baskets_get, baskets_id_get
from aiohttp.web import Application


def setup_routes(app: Application):
    app.router.add_post('/sessions/new', sessions_post, name='login')
    app.router.add_delete('/sessions', sessions_delete, name='logout')

    app.router.add_get('/users', users_get, name='users')
    app.router.add_get('/users/{login}', users_get, name='user_info')
    app.router.add_post('/users', users_post, name='create_user')

    app.router.add_get('/shops', shops_get, name='shops')
    app.router.add_get('/shops/{id}', shops_id_get, name='shop_info')
    app.router.add_post('/shops', shops_post, name='shop_create')
    app.router.add_get('/shops/{id}/products', shops_id_products_get, name='shop_products_info')

    app.router.add_get('/products', products_get, name='products')
    app.router.add_get('/products/{id}', products_id_get, name='product_info')
    app.router.add_post('/products', products_post, name='product_create')
    app.router.add_get('/products/{id}/shops', products_shops_get, name='product_shops_info')
    app.router.add_post('/products/{id}/shops', products_shops_post, name='add_shop_to_product')

    app.router.add_get('/baskets', baskets_get, name='baskets')
    app.router.add_get('/baskets/{id}', baskets_id_get, name='basket_info')

