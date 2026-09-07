from flask import Blueprint, request, jsonify
from app.decorators import login_required
from app.services.category_service import (
    create_category, rename_category, delete_category, list_categories, CategoryError,
)
from app.services.product_service import (
    create_product, update_product, delete_product, list_products, ProductError,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    if request.method == "POST":
        try:
            category = create_category(request.json.get("name", ""))
        except CategoryError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"id": category.id, "name": category.name}), 201
    return jsonify([{"id": c.id, "name": c.name} for c in list_categories()])


@admin_bp.route("/categories/<int:category_id>", methods=["PUT", "DELETE"])
@login_required
def category_detail(category_id):
    try:
        if request.method == "PUT":
            category = rename_category(category_id, request.json.get("name", ""))
            return jsonify({"id": category.id, "name": category.name})
        delete_category(category_id)
        return "", 204
    except CategoryError as e:
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/products", methods=["GET", "POST"])
@login_required
def products():
    if request.method == "POST":
        try:
            product = create_product(request.json)
        except ProductError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"id": product.id, "name": product.name}), 201
    return jsonify([{"id": p.id, "name": p.name} for p in list_products(active_only=False)])


@admin_bp.route("/products/<int:product_id>", methods=["PUT", "DELETE"])
@login_required
def product_detail(product_id):
    try:
        if request.method == "PUT":
            product = update_product(product_id, request.json)
            return jsonify({"id": product.id, "name": product.name})
        delete_product(product_id)
        return "", 204
    except ProductError as e:
        return jsonify({"error": str(e)}), 400
