import os
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Хуучин зөрүүтэй хүснэгтүүдийг хүчээр бүгдийг устгана
        db.drop_all()
        # Шинэ кодын бүтцийн дагуу хүснэгтүүдийг дахин үүсгэнэ
        db.create_all()
        print(">>> BAAZYNG BUKH KHUSNGETIYIIG TGEES NI SHINICLIL EE <<<")
    except Exception as e:
        print(f">>> ERROR: {e} <<<")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)