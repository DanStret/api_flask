from flask import Flask
from app.routes.system_routes import system_bp  # Asegúrate de importar el blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Registrar el blueprint con el prefijo "/api"
    app.register_blueprint(system_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
