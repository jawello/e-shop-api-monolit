from app.models import Users
from app.models import Product
from app.models import Shop
from app.models import ProductShop
from app.models import Basket
from app.models import ProductInBasket
from app.models import Order

from faker import Faker

from app.db import construct_db_url
from app.settings import load_config
from app.security import generate_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import random

import logging

log = logging.getLogger(__name__)


def generate_users(session: Session, count: int) -> list:
    faker = Faker('ru_RU')
    default_pass = generate_password_hash('skytrack')
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
    user_was = set()
    for i in range(count):
        j = 0
        while j < count:
            user = users[random.randint(0, len(users) - 1)]
            if user not in user_was:
                user_was.add(user)
                break
            j = j+1
        if j >= count:
            break
        basket = Basket(users=user)
        session.add(basket)

        result.append(basket)
    session.commit()
    for i in result:
        session.refresh(i)
        log.info(f"Generate basket: {i}")
    return result


def generate_product_in_basket(session: Session, baskets: list, products_shops: list):
    result = []
    for basket in baskets:
        products_in_basket_count = random.randint(1, 20)
        product_was = set()
        for i in range(products_in_basket_count):
            product_shop = products_shops[random.randint(0, len(products_shops) - 1)]
            while product_shop.id in product_was:
                product_shop = products_shops[random.randint(0, len(products_shops) - 1)]

            product_was.add(product_shop.id)
            if product_shop.quantity == 1:
                quantity = 1
            elif product_shop.quantity >= 10:
                quantity = random.randint(1, 10)
            product_in_basket = ProductInBasket(basket=basket,
                                                product_shop=product_shop,
                                                quantity=quantity
                                                )
            session.add(product_in_basket)
            result.append(product_in_basket)

    session.commit()
    for i in result:
        session.refresh(i)
        log.info(f"Generate product_in_basket: {i}")


def generate_order(session: Session, count: int, baskets: list):
    result = []
    statuses = ["check availability", "awaiting payment", "paid"]
    faker = Faker()
    basket_was = set()
    for i in range(count):
        while True:
            basket = baskets[random.randint(0, len(baskets) - 1)]
            if basket not in basket_was:
                basket_was.add(basket)
                break
        status = statuses[random.randint(0, len(statuses) - 1)]
        order = Order(basket=basket, status=status, date=faker.date_time_this_year())
        session.add(order)
        result.append(order)
    session.commit()
    for i in result:
        session.refresh(i)
        log.info(f"Generate order: {i}")


def main(config_path):
    config = load_config(config_path)
    logging.basicConfig(level=logging.INFO)
    db_url = construct_db_url(config['database'])
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = generate_users(session, 100)
    products = generate_products(session, 100)
    shops = generate_shop(session, 10)
    products_shops = generate_product_shop(session, 200, products, shops)
    baskets = generate_basket(session, 50, users)
    generate_product_in_basket(session, baskets, products_shops)
    generate_order(session, 30, baskets)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
