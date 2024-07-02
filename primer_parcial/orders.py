from config import db
from flask import abort, make_response
from models import Order, Customer, order_schema


def read_one(order_id):
    order = Order.query.get(order_id)

    if order is not None:
        return order_schema.dump(order)
    else:
        abort(404, f"Order with ID {order_id} not found")

def create(order):
    customer_id = order.get("customer_id")
    customer = Customer.query.get(customer_id)

    if customer:
        new_order = order_schema.load(order, session=db.session)
        customer.orders.append(new_order)
        db.session.commit()
        return order_schema.dump(new_order), 201
    else:
        abort(404, f"Customer not found for ID: {customer_id}")

def update(order_id, order):
    existing_order = Order.query.get(order_id)

    if existing_order:
        update_order = order_schema.load(order, session=db.session)
        existing_order.content = update_order.content
        db.session.merge(existing_order)
        db.session.commit()
        return order_schema.dump(existing_order), 201
    else:
        abort(404, f"Note with ID {order_id} not found")
        
def delete(order_id):
    existing_order = Order.query.get(order_id)

    if existing_order:
        db.session.delete(existing_order)
        db.session.commit()
        return make_response(f"{order_id} successfully deleted", 204)
    else:
        abort(404, f"Order with ID {order_id} not found")
