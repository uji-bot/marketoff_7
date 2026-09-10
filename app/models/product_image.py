from app.extensions import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    
    # Өгөгдлийн сангийн үндсэн багана (үүнийг гараар оролдох шаардлагагүй)
    _path = db.Column("path", db.String(300), nullable=False)
    
    position = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # HTML темплэйтүүд дээрх {{ image.path }} кодыг автоматаар зохицуулах хэсэг
    @hybrid_property
    def path(self) -> str:
        if self._path and (self._path.startswith('http://') or self._path.startswith('https://')):
            return self._path  # Cloudinary-ийн бүтэн URL бол шууд буцаана
        return f"/static/images/{self._path}"  # Хуучин локал зураг бол хавтасны замыг засаж буцаана

    @path.setter
    def path(self, value: str):
        self._path = value

    def __repr__(self):
        return f"<ProductImage {self._path}>"
