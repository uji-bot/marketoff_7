from app import create_app
from app.extensions import db
from app.services.auth_service import create_admin, AuthError

app = create_app()


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
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
