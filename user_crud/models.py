from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer(), unique=True)
    product_name = db.Column(db.String())
    quantity = db.Column(db.Integer())
    product_category = db.Column(db.String(80))

    def __init__(self, product_id, product_name, quantity, product_category):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.product_category = product_category

    def __repr__(self):
        return f"{self.product_name} | {self.quantity} | " \
               f"{self.product_category}| {self.product_id}"
