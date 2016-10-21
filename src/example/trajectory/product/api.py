from example.trajectory.db import getSession
from example.trajectory.product.model import Product
from example.trajectory.product.model import get_wrapped_product  # noqa


def get_product_by_id(product_id):
    """Given an id, return a SQLAlchemy Produuct object with that id."""
    session = getSession()
    return session.query(Product).filter(Product.id == product_id).scalar()


def add_product(name="", description="", price=0.0):
    """Create a Product object in the sql db."""
    new_product = Product(name=name, description=description, price=price)
    session = getSession()
    session.add(new_product)
    session.commit()
    return new_product
