from app.extensions import db
from datetime import datetime


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    
    # Өгөгдлийн сангийн бодит баганы нэр 'path' хэвээрээ байна
    _path = db.Column("path", db.String(300), nullable=False)
    
    position = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Энгийн Python property болгож өөрчлөв (SQLAlchemy-ийг алдаа заалгахгүй)
    @property
    def path(self) -> str:
        if self._path and (self._path.startswith('http://') or self._path.startswith('https://')):
            return self._path  # Cloudinary URL бол шууд бүтнээр нь буцаана
        return f"/static/images/{self._path}"  # Хуучин локал зураг бол замыг нь засна

    @path.setter
    def path(self, value: str):
        self._path = value

    def __repr__(self):
        return f"<ProductImage {self._path}>"
