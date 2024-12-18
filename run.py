import os
from flask import Flask
from app.routes.system_routes import system_bp  # Importa tus blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Registrar blueprints
    app.register_blueprint(system_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    # Usa el puerto proporcionado por la variable de entorno `PORT` o 5000 como predeterminado
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
