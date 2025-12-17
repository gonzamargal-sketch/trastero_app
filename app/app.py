from flask import Flask
from app.blueprints.main import main_bp
from app.blueprints.objetos import objetos_bp
from app.models import db

app = Flask(__name__)
app.secret_key = "trastero_super_secreto_123"

app.register_blueprint(main_bp)
app.register_blueprint(objetos_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trastero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

