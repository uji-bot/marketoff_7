from app.extensions import db
from app.models.product import Product
from app.models.category import Category


class ProductError(Exception):
    pass


def create_product(data: dict) -> Product:
    name = data.get("name", "").strip()
    if not name:
        raise ProductError("Product name is required")

    price = data.get("price")
    if price is None or price < 0:
        raise ProductError("Valid price is required")

    category_id = data.get("category_id")
    if category_id and not Category.query.get(category_id):
        raise ProductError("Valid category is required")

    product = Product(
        name=name,
        description=data.get("description", ""),
        price=price,
        category_id=category_id or None,
        is_active=data.get("is_active", True),
        contact_phone=(data.get("contact_phone") or "").strip() or None,
        contact_social=(data.get("contact_social") or "").strip() or None,
    )
    db.session.add(product)
    db.session.commit()
    return product


def update_product(product_id: int, data: dict) -> Product:
    product = Product.query.get(product_id)
    if not product:
        raise ProductError(f"Product {product_id} not found")

    if "name" in data:
        name = data["name"].strip()
        if not name:
            raise ProductError("Product name is required")
        product.name = name

    if "price" in data:
        if data["price"] is None or data["price"] < 0:
            raise ProductError("Valid price is required")
        product.price = data["price"]

    if "category_id" in data:
        if data["category_id"] and not Category.query.get(data["category_id"]):
            raise ProductError("Valid category is required")
        product.category_id = data["category_id"] or None

    if "description" in data:
        product.description = data["description"]

    if "is_active" in data:
        product.is_active = data["is_active"]

    if "contact_phone" in data:
        product.contact_phone = (data["contact_phone"] or "").strip() or None

    if "contact_social" in data:
        product.contact_social = (data["contact_social"] or "").strip() or None

    db.session.commit()
    return product


def delete_product(product_id: int) -> None:
    product = Product.query.get(product_id)
    if not product:
        raise ProductError(f"Product {product_id} not found")
    db.session.delete(product)
    db.session.commit()


def get_product(product_id: int) -> Product:
    product = Product.query.get(product_id)
    if not product:
        raise ProductError(f"Product {product_id} not found")
    return product


def list_products(category_id: int = None, active_only: bool = True) -> list[Product]:
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Product.created_at.desc()).all()
    category_id = data.get("category_id")
    if category_id and not Category.query.get(category_id):
        raise ProductError("Valid category is required")

    stock_quantity = data.get("stock_quantity", 0)
    if stock_quantity is None or stock_quantity < 0:
        raise ProductError("Stock quantity must be zero or positive")

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