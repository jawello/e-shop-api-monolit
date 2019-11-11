from app.models import Users
from app.models import Product
from app.models import Shop
from app.models import ProductShop
from app.models import Basket

from faker import Faker

from app.db import construct_db_url
from app.settings import load_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import random

import logging

log = logging.getLogger(__name__)


def generate_users(session: Session, count: int) -> list:
    faker = Faker('ru_RU')
    default_pass = 'skytrack'
    result = []
    for i in range(count):
        fake = faker.simple_profile(sex=None)
        user = Users(name=fake['name'], login=fake['username'], password=default_pass)
        result.append(user)
        log.info(f"Generate user: {user}")
        session.add(user)
    session.commit()
    for i in result:
        session.refresh(i)
    return result


def generate_products(session: Session, count: int) -> list:
    faker = Faker('ru_RU')
    result = []
    for i in range(count):
        name = " ".join(faker.words(nb=3))
        description = faker.texts(nb_texts=3, max_nb_chars=200)
        product = Product(name=name, description=description)
        result.append(product)
        log.info(f"Generate product: {product}")
        session.add(product)
    session.commit()
    for i in result:
        session.refresh(i)
    return result


def generate_shop(session: Session, count: int) -> list:
    faker = Faker()
    result = []
    for i in range(count):
        name = faker.company()
        description = faker.bs()
        site = faker.domain_name()
        shop = Shop(name=name, description=description, site=site)
        result.append(shop)
        log.info(f"Generate shop: {shop}")
        session.add(shop)
    session.commit()
    for i in result:
        session.refresh(i)
    return result


def generate_product_shop(session: Session, count: int, products: list, shops: list) -> list:
    result = []
    for i in range(count):
        shop = shops[random.randint(0, len(shops) - 1)]
        product = products[random.randint(0, len(products) - 1)]
        price = round(random.uniform(5, 4000), 2)
        quantity = random.randint(0, 1000)
        product_shop = ProductShop(product=product, shop=shop, price=price, quantity=quantity)
        try:
            session.add(product_shop)
            session.commit()
        except:
            session.rollback()
            continue
        log.info(f"Generate product_shop: {product_shop}")
        result.append(product_shop)
    for i in result:
        session.refresh(i)
    return result


def generate_basket(session: Session, count: int, users: list) -> list:
    result = []
    for i in range(count):
        user = users[random.randint(0, len(users) - 1)]
        basket = Basket(users=user)
        session.add(basket)

        result.append(basket)
    session.commit()
    for i in result:
        session.refresh(i)
        log.info(f"Generate product_shop: {i}")
    return result


def main(config_path):
    config = load_config(config_path)
    logging.basicConfig(level=logging.INFO)
    db_url = construct_db_url(config['database'])
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = generate_users(session, 10)
    products = generate_products(session, 100)
    shops = generate_shop(session, 10)
    products_shops = generate_product_shop(session, 100, products, shops)
    baskets = generate_basket(session, 100, users)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()

