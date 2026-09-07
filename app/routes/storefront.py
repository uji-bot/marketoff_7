from flask import Blueprint, jsonify, render_template, request
from app.services.product_service import list_products, get_product, ProductError
from app.services.category_service import list_categories

storefront_bp = Blueprint("storefront", __name__)


@storefront_bp.route("/")
def home():
    categories = list_categories()
    category_id = request.args.get("category_id", type=int)
    products = list_products(category_id=category_id)
    return render_template(
        "storefront/home.html",
        categories=categories,
        products=products,
        selected_category=category_id,
    )


@storefront_bp.route("/api/products")
def products_api():
    items = list_products()
    return jsonify([{"id": p.id, "name": p.name, "price": str(p.price)} for p in items])


@storefront_bp.route("/api/products/<int:product_id>")
def product_detail_api(product_id):
    try:
        product = get_product(product_id)
    except ProductError:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"id": product.id, "name": product.name, "price": str(product.price)})

from flask import Blueprint, jsonify, render_template, request
from app.services.product_service import list_products, get_product, ProductError
from app.services.category_service import list_categories

storefront_bp = Blueprint("storefront", __name__)


@storefront_bp.route("/")
def home():
    categories = list_categories()
    category_id = request.args.get("category_id", type=int)
    products = list_products(category_id=category_id)
    return render_template(
        "storefront/home.html",
        categories=categories,
        products=products,
        selected_category=category_id,
    )


@storefront_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    try:
        product = get_product(product_id)
    except ProductError:
        return render_template("storefront/home.html", categories=list_categories(), products=[]), 404
    return render_template("storefront/product_detail.html", product=product)


@storefront_bp.route("/api/products")
def products_api():
    items = list_products()
    return jsonify([{"id": p.id, "name": p.name, "price": str(p.price)} for p in items])