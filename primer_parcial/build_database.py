from datetime import datetime

from config import app, db
from models import Order, Customer

CUSTOMER_NOTES = [
    {
        "lname": "Doe",
        "fname": "John",
        "status": True,
        "email": "johndoe@gmail.com",
        "orders": [],
    },
    {
        "lname": "Roe",
        "fname": "Robert",
        "status": False,
        "email": "roerobert@gmail.com",
        "orders": [
            (
                "5000", "2020-12-06"
            ),
        ],
    },
    {
        "lname": "Sammy",
        "fname": "Soe",
        "status": True,
        "email": "sammysoe@gmail.com",
        "orders": [
            (
                "200", "2020-12-06"
            ),
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in CUSTOMER_NOTES:
        new_customer = Customer(
            lname=data.get("lname"),
            fname=data.get("fname"),
            status=data.get("status"),
            email=data.get("email")
        )
        
        for total_price, order_date in data.get("orders", []):
            new_order = Order(
                total_price=total_price,
                order_date=datetime.strptime(order_date, "%Y-%m-%d").date(),
            )
            new_customer.orders.append(new_order)
        
        db.session.add(new_customer)
    db.session.commit()
