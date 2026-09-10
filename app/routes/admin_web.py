import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from app.decorators import login_required_web
from app.extensions import db
from app.services.category_service import create_category, delete_category, list_categories, CategoryError
from app.services.product_service import create_product, update_product, delete_product, list_products, get_product, ProductError
from app.services.image_service import save_images, delete_image, upload_to_cloudinary, ImageError
from app.services.auth_service import authenticate
from app.models.product import Product
from app.services.sale_service import (
    record_sale, update_sale, delete_sale, SaleError,
    get_sales_detail, get_sales_by_category, total_revenue,
)

admin_web_bp = Blueprint("admin_web", __name__, url_prefix="/admin")

UPLOAD_FOLDER = os.path.join("app", "static", "images")


@admin_web_bp.route("/login", methods=["GET", "POST"])
def login_page():
    error = None
    if request.method == "POST":
        admin = authenticate(request.form.get("username", ""), request.form.get("password", ""))
        if admin:
            session["admin_id"] = admin.id
            return redirect(url_for("admin_web.manage_products"))
        error = "Нэвтрэх мэдээлэл буруу байна"
    return render_template("admin/login.html", error=error)


@admin_web_bp.route("/logout", methods=["POST"])
def logout_page():
    session.pop("admin_id", None)
    return redirect(url_for("admin_web.login_page"))


@admin_web_bp.route("/products/new", methods=["GET", "POST"])
@login_required_web
def new_product_page():
    error = None
    if request.method == "POST":
        try:
            product = create_product({
                "name": request.form.get("name", ""),
                "price": float(request.form.get("price", 0) or 0),
                "category_id": int(request.form.get("category_id") or 0) or None,
                "description": request.form.get("description", ""),
                "contact_phone": request.form.get("contact_phone", ""),
                "contact_social": request.form.get("contact_social", ""),
                "stock_quantity": int(request.form.get("stock_quantity", 0) or 0),
            })
            files = [f for f in request.files.getlist("images") if f.filename]
            if files:
                uploaded_urls = [upload_to_cloudinary(f) for f in files]
                save_images(product.id, uploaded_urls)
            return redirect(url_for("admin_web.manage_products"))
        except (ProductError, ImageError, ValueError) as e:
            error = str(e)

    categories = list_categories()
    return render_template("admin/product_form.html", categories=categories, error=error, product=None)


@admin_web_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required_web
def edit_product_page(product_id):
    try:
        product = get_product(product_id)
    except ProductError:
        return redirect(url_for("admin_web.manage_products"))

    error = None
    if request.method == "POST":
        try:
            update_product(product_id, {
                "name": request.form.get("name", ""),
                "price": float(request.form.get("price", 0) or 0),
                "category_id": int(request.form.get("category_id") or 0) or None,
                "description": request.form.get("description", ""),
                "contact_phone": request.form.get("contact_phone", ""),
                "contact_social": request.form.get("contact_social", ""),
                "stock_quantity": int(request.form.get("stock_quantity", 0) or 0),
            })

            files = [f for f in request.files.getlist("images") if f.filename]
            if files:
                uploaded_urls = [upload_to_cloudinary(f) for f in files]
                save_images(product.id, uploaded_urls)

            return redirect(url_for("admin_web.manage_products"))
        except (ProductError, ImageError, ValueError) as e:
            error = str(e)

    categories = list_categories()
    return render_template("admin/product_form.html", categories=categories, error=error, product=product)


@admin_web_bp.route("/products/<int:product_id>/images/<int:image_id>/delete", methods=["POST"])
@login_required_web
def delete_product_image(product_id, image_id):
    try:
        delete_image(image_id)
    except ImageError:
        pass
    return redirect(url_for("admin_web.edit_product_page", product_id=product_id))


@admin_web_bp.route("/products")
@login_required_web
def manage_products():
    products = list_products(active_only=False)
    categories = list_categories()
    error = request.args.get("error")
    return render_template("admin/products_list.html", products=products, categories=categories, error=error)


@admin_web_bp.route("/products/<int:product_id>/sale", methods=["POST"])
@login_required_web
def record_sale_web(product_id):
    try:
        quantity = int(request.form.get("quantity", 1) or 1)
        record_sale(product_id, quantity)
    except (SaleError, ValueError):
        db.session.rollback()
    return redirect(url_for("admin_web.manage_products"))


@admin_web_bp.route("/sales")
@login_required_web
def sales_report_page():
    sales = get_sales_detail()
    by_category = get_sales_by_category()
    total = total_revenue()
    products = list_products(active_only=False)
    return render_template(
        "admin/sales_report.html",
        sales=sales, by_category=by_category, total=total, products=products,
    )


@admin_web_bp.route("/sales/add", methods=["POST"])
@login_required_web
def add_sale_web():
    try:
        name = request.form.get("product_name", "").strip()
        product = Product.query.filter(Product.name.ilike(name)).first()
        if not product:
            return redirect(url_for("admin_web.sales_report_page"))
        quantity = int(request.form.get("quantity", 1) or 1)
        price = request.form.get("price")
        price = float(price) if price else None
        record_sale(product.id, quantity, price)
    except (SaleError, ValueError, TypeError):
        db.session.rollback()
    return redirect(url_for("admin_web.sales_report_page"))


@admin_web_bp.route("/sales/<int:sale_id>/edit", methods=["POST"])
@login_required_web
def edit_sale_web(sale_id):
    try:
        quantity = int(request.form.get("quantity", 1) or 1)
        price = float(request.form.get("price", 0) or 0)
        update_sale(sale_id, quantity=quantity, price=price)
    except (SaleError, ValueError):
        db.session.rollback()
    return redirect(url_for("admin_web.sales_report_page"))


@admin_web_bp.route("/sales/<int:sale_id>/delete", methods=["POST"])
@login_required_web
def delete_sale_web(sale_id):
    try:
        delete_sale(sale_id)
    except SaleError:
        db.session.rollback()
    return redirect(url_for("admin_web.sales_report_page"))


@admin_web_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required_web
def delete_product_web(product_id):
    try:
        delete_product(product_id)
    except ProductError:
        pass
    return redirect(url_for("admin_web.manage_products"))


@admin_web_bp.route("/categories/new", methods=["POST"])
@login_required_web
def new_category():
    try:
        create_category(request.form.get("name", ""))
    except CategoryError:
        pass
    return redirect(url_for("admin_web.manage_products"))


@admin_web_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required_web
def delete_category_web(category_id):
    try:
        delete_category(category_id)
    except CategoryError as e:
        return redirect(url_for("admin_web.manage_products", error=str(e)))
    return redirect(url_for("admin_web.manage_products"))
