import pytest
from app.services.category_service import (
    create_category, rename_category, delete_category,
    list_categories, CategoryError,
)


def test_create_category(db_session):
    cat = create_category("Parfum")
    assert cat.id is not None
    assert cat.slug == "parfum"


def test_create_duplicate_category_raises(db_session):
    create_category("Parfum")
    with pytest.raises(CategoryError):
        create_category("Parfum")


def test_rename_category(db_session):
    cat = create_category("Parfum")
    updated = rename_category(cat.id, "Perfume")
    assert updated.name == "Perfume"


def test_delete_category(db_session):
    cat = create_category("Parfum")
    delete_category(cat.id)
    assert list_categories() == []