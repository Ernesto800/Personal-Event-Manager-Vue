from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    database_path = os.path.join(app.instance_path, 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['JWT_SECRET_KEY'] = "TESTKEY123" 
    print(f"DEBUG: JWT_SECRET_KEY cargada (directamente): '{app.config['JWT_SECRET_KEY']}' (Tipo: {type(app.config['JWT_SECRET_KEY'])})")


    if not app.config['JWT_SECRET_KEY']:
        raise RuntimeError("JWT_SECRET_KEY no está configurada. Por favor, asegúrate de añadirla en tu archivo .env en la raíz de la carpeta 'backend/'.")

    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ALGORITHM'] = 'HS256'
    print(f"DEBUG: JWT_ALGORITHM configurado: '{app.config['JWT_ALGORITHM']}'")

    CORS(app, resources={r"/api/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }})

    db.init_app(app)
    jwt.init_app(app) 
    migrate.init_app(app, db)

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        print("DEBUG: unauthorized_loader activado.")
        return jsonify({"message": "Token de acceso ausente o no válido"}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        print("DEBUG: invalid_token_loader activado.")
        return jsonify({"message": "Token de acceso inválido"}), 401
    
    @jwt.expired_token_loader
    def expired_token_response(callback):
        print("DEBUG: expired_token_loader activado.")
        return jsonify({"message": "Token de acceso expirado"}), 401

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    from app.routes.auth import auth_bp
    from app.routes.events import events_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(events_bp, url_prefix='/api')

    return app