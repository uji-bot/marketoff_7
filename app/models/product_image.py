from app.extensions import db
from datetime import datetime


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    
    # Бодит баганы нэрийг 'path' хэвээр нь цэвэрхэн буцааж тавив. (Алдаа арилна)
    path = db.Column(db.String(300), nullable=False)
    
    position = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # HTML темплэйтүүд дээр найдвартай унших шинэ ухаалаг шинж чанар
    @property
    def display_url(self) -> str:
        if self.path and (self.path.startswith('http://') or self.path.startswith('https://')):
            return self.path  # Cloudinary URL бол шууд бүтнээр нь буцаана
        return f"/static/images/{self.path}"  # Хуучин локал зураг бол хавтасны замыг засна

    def __repr__(self):
        return f"<ProductImage {self.path}>"
