from app.extensions import db
from app.models.product import Product
from app.models.category import Category


class ProductError(Exception):
    pass


def create_product(data: dict) -> Product:
    try:
        name = data.get("name", "").strip()
        if not name:
            raise ProductError("Бүтээгдэхүүний нэр заавал хэрэгтэй")

        price = data.get("price")
        if price is None or price < 0:
            raise ProductError("Үнийн дүн буруу байна")

        category_id = data.get("category_id")
        if category_id and not Category.query.get(category_id):
            raise ProductError("Сонгосон категори олдсонгүй")

        stock_quantity = data.get("stock_quantity", 0)
        if stock_quantity is None or stock_quantity < 0:
            raise ProductError("Үлдэгдэл тоо хэмжээ хасах байж болохгүй")

        product = Product(
            name=name,
            description=data.get("description", ""),
            price=price,
            category_id=category_id or None,
            is_active=data.get("is_active", True),
            contact_phone=(data.get("contact_phone") or "").strip() or None,
            contact_social=(data.get("contact_social") or "").strip() or None,
            stock_quantity=stock_quantity,
        )
        db.session.add(product)
        db.session.commit()
        return product
    except Exception as e:
        db.session.rollback()  # Алдаа гарвал өгөгдлийн сангийн сессийг цэвэрлэнэ
        if not isinstance(e, ProductError):
            raise ProductError(f"Хадгалахад алдаа гарлаа: {str(e)}")
        raise e


def update_product(product_id: int, data: dict) -> Product:
    try:
        product = Product.query.get(product_id)
        if not product:
            raise ProductError(f"Бүтээгдэхүүн {product_id} олдсонгүй")

        if "name" in data:
            name = data["name"].strip()
            if not name:
                raise ProductError("Бүтээгдэхүүний нэр заавал хэрэгтэй")
            product.name = name

        if "price" in data:
            if data["price"] is None or data["price"] < 0:
                raise ProductError("Үнийн дүн буруу байна")
            product.price = data["price"]

        if "category_id" in data:
            if data["category_id"] and not Category.query.get(data["category_id"]):
                raise ProductError("Сонгосон категори олдсонгүй")
            product.category_id = data["category_id"] or None

        if "description" in data:
            product.description = data["description"]

        if "is_active" in data:
            product.is_active = data["is_active"]

        if "contact_phone" in data:
            product.contact_phone = (data["contact_phone"] or "").strip() or None

        if "contact_social" in data:
            product.contact_social = (data["contact_social"] or "").strip() or None

        if "stock_quantity" in data:
            stock_quantity = data["stock_quantity"]
            if stock_quantity is None or stock_quantity < 0:
                raise ProductError("Үлдэгдэл тоо хэмжээ хасах байж болохгүй")
            product.stock_quantity = stock_quantity

        db.session.commit()
        return product
    except Exception as e:
        db.session.rollback()  # Алдаа гарвал буцаана
        if not isinstance(e, ProductError):
            raise ProductError(f"Шинэчлэхэд алдаа гарлаа: {str(e)}")
        raise e


def delete_product(product_id: int) -> None:
    try:
        product = Product.query.get(product_id)
        if not product:
            raise ProductError(f"Бүтээгдэхүүн {product_id} олдсонгүй")
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ProductError(f"Устгахад алдаа гарлаа: {str(e)}")


def get_product(product_id: int) -> Product:
    product = Product.query.get(product_id)
    if not product:
        raise ProductError(f"Бүтээгдэхүүн {product_id} олдсонгүй")
    return product


def list_products(category_id: int = None, active_only: bool = True) -> list[Product]:
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Product.created_at.desc()).all()
