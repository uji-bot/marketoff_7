from app.extensions import db
from datetime import datetime


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Numeric(10, 2), nullable=False)
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale product={self.product_id} qty={self.quantity}>"