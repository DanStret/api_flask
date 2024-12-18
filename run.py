import os
from flask import Flask
from app.routes.system_routes import system_bp  # Importar el blueprint correctamente

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Registrar el blueprint con el prefijo "/api"
    app.register_blueprint(system_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Obtener el puerto dinámicamente de Render
    app.run(host="0.0.0.0", port=port, debug=False)  # Configurar host y puerto
