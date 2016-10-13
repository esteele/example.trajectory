from example.trajectory.db import getSession
from example.trajectory.product.model import Product


def get_product_by_id(product_id):
    session = getSession()
    return session.query(Product).filter(Product.id == product_id).scalar()


def add_product(name="", description="", price=0.0):
    new_product = Product(name=name, description=description, price=price)
    session = getSession()
    session.add(new_product)
    session.commit()
    return new_product
