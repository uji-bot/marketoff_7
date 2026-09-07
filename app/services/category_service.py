import re
from app.extensions import db
from app.models.category import Category


class CategoryError(Exception):
    pass


def _slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9\u0400-\u04FF]+", "-", slug)
    return slug.strip("-")


def create_category(name: str) -> Category:
    name = name.strip()
    if not name:
        raise CategoryError("Category name is required")

    slug = _slugify(name)
    if Category.query.filter_by(slug=slug).first():
        raise CategoryError(f"Category '{name}' already exists")

    category = Category(name=name, slug=slug)
    db.session.add(category)
    db.session.commit()
    return category


def rename_category(category_id: int, new_name: str) -> Category:
    category = Category.query.get(category_id)
    if not category:
        raise CategoryError(f"Category {category_id} not found")

    new_name = new_name.strip()
    if not new_name:
        raise CategoryError("Category name is required")

    new_slug = _slugify(new_name)
    existing = Category.query.filter_by(slug=new_slug).first()
    if existing and existing.id != category_id:
        raise CategoryError(f"Category '{new_name}' already exists")

    category.name = new_name
    category.slug = new_slug
    db.session.commit()
    return category


def delete_category(category_id: int) -> None:
    category = Category.query.get(category_id)
    if not category:
        raise CategoryError(f"Category {category_id} not found")

    for product in category.products:
        product.category_id = None

    db.session.delete(category)
    db.session.commit()


def list_categories() -> list[Category]:
    return Category.query.order_by(Category.name).all()
