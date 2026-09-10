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
    try:
        name = name.strip()
        if not name:
            raise CategoryError("Категорийн нэр заавал хэрэгтэй")

        slug = _slugify(name)
        if Category.query.filter_by(slug=slug).first():
            raise CategoryError(f"'{name}' нэртэй категори аль хэдийн үүссэн байна")

        category = Category(name=name, slug=slug)
        db.session.add(category)
        db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        if not isinstance(e, CategoryError):
            raise CategoryError(f"Категори үүсгэхэд алдаа гарлаа: {str(e)}")
        raise e


def rename_category(category_id: int, new_name: str) -> Category:
    try:
        category = Category.query.get(category_id)
        if not category:
            raise CategoryError(f"Категори {category_id} олдсонгүй")

        new_name = new_name.strip()
        if not new_name:
            raise CategoryError("Категорийн нэр заавал хэрэгтэй")

        new_slug = _slugify(new_name)
        existing = Category.query.filter_by(slug=new_slug).first()
        if existing and existing.id != category_id:
            raise CategoryError(f"'{new_name}' нэртэй категори аль хэдийн үүссэн байна")

        category.name = new_name
        category.slug = new_slug
        db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        if not isinstance(e, CategoryError):
            raise CategoryError(f"Категорийн нэр өөрчлөхөд алдаа гарлаа: {str(e)}")
        raise e


def delete_category(category_id: int) -> None:
    try:
        category = Category.query.get(category_id)
        if not category:
            raise CategoryError(f"Категори {category_id} олдсонгүй")

        for product in category.products:
            product.category_id = None

        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise CategoryError(f"Категори устгахад алдаа гарлаа: {str(e)}")


def list_categories() -> list[Category]:
    return Category.query.order_by(Category.name).all()
