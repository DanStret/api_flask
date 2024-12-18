from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

# Ruta de prueba para autenticación
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not "username" in data or not "password" in data:
        return jsonify({"message": "Username and password are required"}), 400

    # Simulación de autenticación
    if data["username"] == "admin" and data["password"] == "1234":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
