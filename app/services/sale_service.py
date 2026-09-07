from app.extensions import db
from app.models.sale import Sale
from app.models.product import Product


class SaleError(Exception):
    pass


def record_sale(product_id: int, quantity: int, price: float = None) -> Sale:
    product = Product.query.get(product_id)
    if not product:
        raise SaleError(f"Product {product_id} not found")

    if quantity is None or quantity <= 0:
        raise SaleError("Quantity must be a positive number")

    sale = Sale(
        product_id=product_id,
        quantity=quantity,
        price_at_sale=price if price is not None else product.price,
    )
    db.session.add(sale)
    db.session.commit()
    return sale


def get_sales_report(start_date=None, end_date=None) -> list[Sale]:
    query = Sale.query
    if start_date:
        query = query.filter(Sale.sold_at >= start_date)
    if end_date:
        query = query.filter(Sale.sold_at <= end_date)
    return query.order_by(Sale.sold_at.desc()).all()


def total_revenue(start_date=None, end_date=None) -> float:
    sales = get_sales_report(start_date, end_date)
    return sum(float(s.price_at_sale) * s.quantity for s in sales)