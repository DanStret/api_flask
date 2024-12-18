from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

system_bp = Blueprint("systems", __name__)

# 1. Obtener todos los edificios
@system_bp.route("/edificios", methods=["GET"])
def get_edificios():
    try:
        query = text("""
            SELECT id_edificio, nombre, direccion, ubicacion, estatus
            FROM edificios
        """)
        result = db.session.execute(query).fetchall()

        edificios = [
            {"id_edificio": row.id_edificio, "nombre": row.nombre, "direccion": row.direccion,
             "ubicacion": row.ubicacion, "estatus": row.estatus}
            for row in result
        ]
        return jsonify({"status": "success", "edificios": edificios}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener edificios: {str(e)}"}), 500


# 2. Obtener pisos por edificio específico
@system_bp.route("/pisos", methods=["GET"])
def get_pisos_by_edificio():
    try:
        id_edificio = request.args.get("id_edificio")

        if not id_edificio:
            return jsonify({"status": "error", "message": "Se requiere el parámetro id_edificio"}), 400

        query = text("""
            SELECT id_piso, nombre
            FROM pisos
            WHERE id_edificio = :id_edificio
        """)
        result = db.session.execute(query, {"id_edificio": id_edificio}).fetchall()

        pisos = [{"id_piso": row.id_piso, "nombre": row.nombre} for row in result]
        return jsonify({"status": "success", "pisos": pisos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener pisos: {str(e)}"}), 500


# 3. Obtener sistemas por edificio/piso (Chiller incluido)
@system_bp.route("/sistemas", methods=["GET"])
def get_sistemas_by_edificio_piso():
    try:
        id_edificio = request.args.get("id_edificio")
        id_piso = request.args.get("id_piso")

        if not id_edificio:
            return jsonify({"status": "error", "message": "Se requiere al menos el parámetro id_edificio"}), 400

        # Consulta dinámica
        query = """
            SELECT s.id_sistema, s.nombre AS nombre_sistema, s.tipo, s.estatus, s.fecha_instalacion
            FROM sistemas s
            LEFT JOIN pisos p ON s.id_piso = p.id_piso
            LEFT JOIN edificios e ON p.id_edificio = e.id_edificio OR s.id_piso IS NULL
        """
        filters = ["e.id_edificio = :id_edificio"]
        params = {"id_edificio": id_edificio}

        if id_piso:
            filters.append("p.id_piso = :id_piso")
            params["id_piso"] = id_piso

        # Agregar filtros dinámicos
        query += " WHERE " + " AND ".join(filters)

        result = db.session.execute(text(query), params).fetchall()

        sistemas = [
            {"id_sistema": row.id_sistema, "nombre_sistema": row.nombre_sistema, "tipo": row.tipo,
             "estatus": row.estatus, "fecha_instalacion": row.fecha_instalacion}
            for row in result
        ]
        return jsonify({"status": "success", "sistemas": sistemas}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener sistemas: {str(e)}"}), 500

@system_bp.route("/sistemas/detalle/<int:id_sistema>", methods=["GET"])
def get_sistema_detalle(id_sistema):
    try:
        query = text("""
            SELECT id_sistema, nombre, tipo, estatus, fecha_instalacion
            FROM sistemas
            WHERE id_sistema = :id_sistema
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({"status": "error", "message": "Sistema no encontrado"}), 404

        sistema = {
            "id_sistema": result.id_sistema,
            "nombre": result.nombre,
            "tipo": result.tipo,
            "estatus": result.estatus,
            "fecha_instalacion": result.fecha_instalacion,
        }
        return jsonify({"status": "success", "sistema": sistema}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@system_bp.route("/presurizacion/<int:id_sistema>", methods=["GET"])
def get_latest_data_presurizacion(id_sistema):
    try:
        query = text("""
            SELECT id, timestamp, tensionMotor, tensionDC, Corriente, Potencia, Frecuencia, Temperatura, IA, AV
            FROM data_presurizacion
            WHERE id_sistema = :id_sistema
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({"status": "error", "message": "No se encontraron datos para el sistema especificado"}), 404

        # Formatear los datos del último registro
        data = {
            "id": result.id,
            "timestamp": result.timestamp,
            "tensionMotor": result.tensionMotor,
            "tensionDC": result.tensionDC,
            "corriente": result.Corriente,
            "potencia": result.Potencia,
            "frecuencia": result.Frecuencia,
            "temperatura": result.Temperatura,
            "IA": result.IA,
            "AV": result.AV,
        }
        return jsonify({"status": "success", "data_presurizacion": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
