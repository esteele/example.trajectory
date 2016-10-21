from example.trajectory.db import getSession
from example.trajectory.customer.model import Customer


def get_customer_by_id(customer_id):
    session = getSession()
    return session.query(Customer).filter(Customer.id == customer_id).scalar()


def add_customer(firstname=None, lastname=None, email=None, address=None):
    new_customer = Customer(firstname=firstname, lastname=lastname, email=email, address=address)
    session = getSession()
    session.add(new_customer)
    session.commit()
    return new_customer
