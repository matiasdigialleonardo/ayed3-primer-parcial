from datetime import datetime

from config import db, ma
from marshmallow_sqlalchemy import fields


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False) 


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(50), unique=True, nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    orders = db.relationship(
        Order,
        backref="customer",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Order.order_date)",
    )


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    orders = fields.Nested(OrderSchema, many=True)


order_schema = OrderSchema()
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
