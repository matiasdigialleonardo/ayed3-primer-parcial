from config import db
from flask import abort, make_response
from models import Customer, customers_schema, customer_schema


def read_all():
    customers = Customer.query.all()
    return customers_schema.dump(customers)

def create(customer):
    lname = customer.get("lname")
    existing_customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if existing_customer is None:
        new_customer = customer_schema.load(customer, session=db.session)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer), 201
    else:
        abort(406, f"Person with last name {lname} already exists")
        
def read_one(lname):
    customer = Customer.query.filter(Customer.lname == lname).one_or_none()
    
    if customer is not None:
        return customer_schema.dump(customer)
    else:
        abort(404, f"Customer with last name {lname} not found")


def update(lname, customer):
    existing_customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if existing_customer:
        update_customer = customer_schema.load(customer, session=db.session)
        existing_customer.fname = update_customer.fname
        existing_customer.email = update_customer.email
        existing_customer.status = update_customer.status
        db.session.merge(existing_customer)
        db.session.commit()
        return customer_schema.dump(existing_customer), 201
    else:
        abort(404, f"Customer with last name {lname} not found")


def delete(lname):
    existing_customer = Customer.query.filter(Customer.lname == lname).one_or_none()

    if existing_customer:
        db.session.delete(existing_customer)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Customer with last name {lname} not found")
