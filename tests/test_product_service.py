import pytest
from app.services.category_service import create_category
from app.services.product_service import (
    create_product, update_product, delete_product,
    get_product, list_products, ProductError,
)


@pytest.fixture
def category(db_session):
    return create_category("Parfum")


def test_create_product(db_session, category):
    product = create_product({"name": "Chanel №5", "price": 450000, "category_id": category.id})
    assert product.id is not None
    assert product.is_active is True


def test_create_product_missing_name_raises(db_session, category):
    with pytest.raises(ProductError):
        create_product({"name": "", "price": 100, "category_id": category.id})


def test_create_product_invalid_category_raises(db_session):
    with pytest.raises(ProductError):
        create_product({"name": "Test", "price": 100, "category_id": 999})


def test_update_product(db_session, category):
    product = create_product({"name": "Old", "price": 100, "category_id": category.id})
    updated = update_product(product.id, {"name": "New", "price": 200})
    assert updated.name == "New"


def test_delete_product(db_session, category):
    product = create_product({"name": "Test", "price": 100, "category_id": category.id})
    delete_product(product.id)
    with pytest.raises(ProductError):
        get_product(product.id)


def test_list_products_filters_active(db_session, category):
    create_product({"name": "A", "price": 100, "category_id": category.id})
    p2 = create_product({"name": "B", "price": 100, "category_id": category.id, "is_active": False})
    active = list_products()
    assert p2 not in active