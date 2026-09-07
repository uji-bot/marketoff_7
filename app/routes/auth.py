from flask import Blueprint, request, jsonify, session
from app.services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    admin = authenticate(request.json.get("username", ""), request.json.get("password", ""))
    if not admin:
        return jsonify({"error": "Invalid credentials"}), 401
    session["admin_id"] = admin.id
    return jsonify({"message": "Logged in"})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("admin_id", None)
    return jsonify({"message": "Logged out"})