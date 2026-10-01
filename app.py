from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.usuario_routes import usuario_bp 
from routes.auth_routes import auth_bp
from routes.viaje_routes import viaje_bp
from routes.reserva_routes import reserva_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app) 
    
    # Durante el laboratorio se registrarán aquí los Blueprints.
    app.register_blueprint(auth_bp) 
    app.register_blueprint(usuario_bp)
    app.register_blueprint(viaje_bp)
    app.register_blueprint(reserva_bp)

    @app.get("/")
    def inicio():
        return {
            "data": {
                "app": "CampusGo API REST",
                "version": "base-laboratorio"
            },
            "message": "API base ejecutándose correctamente",
            "status": True
        }, 200

    
    return app

app = create_app()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
