import os
from app import create_app, db
from app.models.admin_user import AdminUser

app = create_app()

with app.app_context():
    try:
        db.create_all()
        # Burmaa7 админыг сервер асах бүрд шалгаж үүсгэнэ
        admin = AdminUser.query.filter_by(username='Burmaa7').first()
        if not admin:
            admin = AdminUser(username='Burmaa7')
            db.session.add(admin)
        
        admin.set_password('Power@777')
        db.session.commit()
        print(">>> ADMIN USER BURMAA7 IS READY <<<")
    except Exception as e:
        print(f">>> ERROR: {e} <<<")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)