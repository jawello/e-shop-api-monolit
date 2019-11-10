#m aiohttp import web
from UUA.User import UUA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#async def handle(request):
#    name = request.match_info.get('name', "Anonymous")
#    text = "Hello, " + name
#    return web.Response(text=text)

#app = web.Application()
#app.add_routes([web.get('/', handle),
#                web.get('/{name}', handle)])

#if __name__ == '__main__':

engine = create_engine('postgresql://postgres:skytrack@localhost/postgres')


session = sessionmaker()

session.configure(bind=engine)

u = UUA(name='loh', login='loh', password='loh')
s = session()
""":type: sqlalchemy.orm.Session"""
s.add(u)
s.commit()
print(s.query(UUA).all())
#    web.run_app(app)

