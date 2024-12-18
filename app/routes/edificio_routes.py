from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db

edificio_bp = Blueprint("edificios", __name__)

@edificio_bp.route("/", methods=["GET"])
def get_edificios():
    try:
        # Consulta SQL para obtener todos los edificios
        query = text("""
            SELECT id_edificio, nombre, direccion
            FROM edificios
        """)
        result = db.session.execute(query).fetchall()

        # Formatear resultado como lista de diccionarios
        edificios = [
            {"id_edificio": row[0], "nombre": row[1], "direccion": row[2]}
            for row in result
        ]

        return jsonify({"status": "success", "edificios": edificios}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
