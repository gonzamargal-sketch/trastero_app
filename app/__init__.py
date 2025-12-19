import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Ruta absoluta al proyecto
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.join(basedir, "instance", "trastero.db")
    
    # Configuración de la app
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "trastero_super_secreto_123"
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app)  # Permite peticiones desde app móvil

    # Registrar blueprints
    from .blueprints.objetos import objetos_bp
    app.register_blueprint(objetos_bp, url_prefix="/objetos")

    return app




