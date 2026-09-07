from flask import Flask
from app.extensions import db


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    from app.models import category, product, product_image, sale, admin_user

    from app.routes.storefront import storefront_bp
    from app.routes.admin import admin_bp
    from app.routes.admin_web import admin_web_bp

    app.register_blueprint(storefront_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_web_bp)

    return app
