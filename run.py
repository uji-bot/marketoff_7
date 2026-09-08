import os
from app import create_app, db
from app.services.auth_service import create_admin, AuthError

app = create_app()

# Сервер асах болгонд баазын хүснэгтүүдийг кодын дагуу шалгаж үүсгэнэ
with app.app_context():
    db.create_all()

@app.cli.command("create-admin")
def create_admin_command():
    import getpass
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    try:
        create_admin(username, password)
        print(f"Admin '{username}' created.")
    except AuthError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)