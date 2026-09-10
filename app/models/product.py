from app.extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    contact_phone = db.Column(db.String(30), nullable=True)
    contact_social = db.Column(db.String(200), nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship(
        "ProductImage", backref="product", lazy=True,
        cascade="all, delete-orphan", order_by="ProductImage.position"
    )

    # Ухаалаг туслах функц: Хэрэв HTML дээр product.image_path эсвэл ганц тоогоор дуудвал
    # Автоматаар хамгийн эхний зургийн замыг буцаана. Зураггүй бол default зураг заана.
    @property
    def image_path(self) -> str:
        if self.images and len(self.images) > 0:
            return self.images[0].path  # Эхний зургийн URL эсвэл локал замыг авна
        return "/static/images/no-image.png"  # Зураггүй үед харуулах бэлэн зураг

    def __repr__(self):
        return f"<Product {self.name}>"
