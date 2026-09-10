from app.extensions import db
from datetime import datetime


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    
    # Өгөгдлийн сангийн бодит багана
    path = db.Column(db.String(300), nullable=False)
    
    position = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # CLOUDINARY-ИЙН ЗӨВ СЕРВЕР ЗАМТАЙ ЭЦСИЙН ШИЙДЭЛ:
    @property
    def display_url(self) -> str:
        if not self.path:
            return "/static/images/no-image.png"
            
        # 1. Хэрэв аль хэдийн бүтэн URL хаяг (http/https) байвал шууд буцаана
        if self.path.startswith('http://') or self.path.startswith('https://'):
            return self.path
            
        # 2. Хэрэв өгөгдлийн санд зөвхөн ID нэр эсвэл 'marketoff/id.jpg' хэлбэрээр байвал
        # Зөв хувилбар: ://cloudinary.com урд нь заавал байна!
        if '.' in self.path and not self.path.startswith('/'):
            if 'marketoff/' in self.path:
                return f"https://cloudinary.com{self.path}"
            return f"https://cloudinary.commarketoff/{self.path}"
            
        # 3. Хуучин локал хавтасны зураг бол хуучин замаар нь уншина
        return f"/static/images/{self.path}"

    def __repr__(self):
        return f"<ProductImage {self.path}>"
