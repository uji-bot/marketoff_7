import pytest
from app.services.category_service import create_category
from app.services.product_service import create_product
from app.services.sale_service import record_sale, get_sales_report, total_revenue, SaleError


@pytest.fixture
def product(db_session):
    category = create_category("Parfum")
    return create_product({"name": "Test", "price": 100, "category_id": category.id})


def test_record_sale(db_session, product):
    sale = record_sale(product.id, quantity=2)
    assert sale.id is not None
    assert float(sale.price_at_sale) == 100


def test_record_sale_invalid_product_raises(db_session):
    with pytest.raises(SaleError):
        record_sale(999, quantity=1)


def test_record_sale_zero_quantity_raises(db_session, product):
    with pytest.raises(SaleError):
        record_sale(product.id, quantity=0)


def test_get_sales_report(db_session, product):
    record_sale(product.id, quantity=1)
    record_sale(product.id, quantity=2)
    report = get_sales_report()
    assert len(report) == 2


def test_total_revenue(db_session, product):
    record_sale(product.id, quantity=2, price=100)
    record_sale(product.id, quantity=1, price=50)
    assert total_revenue() == 250