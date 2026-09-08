import os
from app import create_app, db
from sqlalchemy import text

app = create_app()

# PostgreSQL URI-г SQLAlchemy-д тохирох хэлбэрт оруулж шинэчлэх
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://", 1)

with app.app_context():
    try:
        # Бааз руу хүчээр шууд холбогдож хүснэгтүүдийг шалгаж үүсгэнэ
        db.create_all()
        print(">>> BAAZYNG KHUSNGETYUD AMJIL TTAI SHINECLEGDLEE <<<")
    except Exception as e:
        print(f">>> ERROR: {e} <<<")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)