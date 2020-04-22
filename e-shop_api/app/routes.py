from endpoints.sessions import sessions_post, sessions_delete
from endpoints.users import users_get, users_post
from aiohttp.web import Application


def setup_routes(app: Application):
    app.router.add_post('/sessions/new', sessions_post, name='login')
    app.router.add_delete('/sessions', sessions_delete, name='logout')

    app.router.add_get('/users', users_get, name='users')
    app.router.add_get('/users/{login}', users_get, name='user_info')
    app.router.add_post('/users', users_post, name='create_user')

