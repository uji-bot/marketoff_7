from app.extensions import db
from app.models.sale import Sale
from app.models.product import Product
from app.models.category import Category


class SaleError(Exception):
    pass


def record_sale(product_id: int, quantity: int, price: float = None) -> Sale:
    product = Product.query.get(product_id)
    if not product:
        raise SaleError(f"Product {product_id} not found")

    if quantity is None or quantity <= 0:
        raise SaleError("Quantity must be a positive number")

    if product.stock_quantity < quantity:
        raise SaleError(f"Insufficient stock: only {product.stock_quantity} left")

    product.stock_quantity -= quantity

    sale = Sale(
        product_id=product_id,
        quantity=quantity,
        price_at_sale=price if price is not None else product.price,
    )
    db.session.add(sale)
    db.session.commit()
    return sale


def update_sale(sale_id: int, quantity: int = None, price: float = None) -> Sale:
    sale = Sale.query.get(sale_id)
    if not sale:
        raise SaleError(f"Sale {sale_id} not found")

    product = Product.query.get(sale.product_id)

    if quantity is not None and quantity != sale.quantity:
        if quantity <= 0:
            raise SaleError("Quantity must be a positive number")
        diff = quantity - sale.quantity
        if product:
            if diff > 0 and product.stock_quantity < diff:
                raise SaleError(f"Insufficient stock: only {product.stock_quantity} left")
            product.stock_quantity -= diff
        sale.quantity = quantity

    if price is not None:
        sale.price_at_sale = price

    db.session.commit()
    return sale


def delete_sale(sale_id: int) -> None:
    sale = Sale.query.get(sale_id)
    if not sale:
        raise SaleError(f"Sale {sale_id} not found")

    product = Product.query.get(sale.product_id)
    if product:
        product.stock_quantity += sale.quantity

    db.session.delete(sale)
    db.session.commit()


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


def get_sales_detail(start_date=None, end_date=None):
    query = db.session.query(Sale, Product).join(Product, Sale.product_id == Product.id)
    if start_date:
        query = query.filter(Sale.sold_at >= start_date)
    if end_date:
        query = query.filter(Sale.sold_at <= end_date)
    return query.order_by(Sale.sold_at.desc()).all()


def get_sales_by_category(start_date=None, end_date=None):
    query = db.session.query(
        Category.name.label("category_name"),
        db.func.sum(Sale.quantity * Sale.price_at_sale).label("revenue"),
        db.func.sum(Sale.quantity).label("qty"),
    ).select_from(Sale).join(Product, Sale.product_id == Product.id).outerjoin(
        Category, Product.category_id == Category.id
    ).group_by(Category.name)

    if start_date:
        query = query.filter(Sale.sold_at >= start_date)
    if end_date:
        query = query.filter(Sale.sold_at <= end_date)
    return query.all()