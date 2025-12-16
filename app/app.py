from flask import Flask
from app.blueprints.main import main_bp
from app.blueprints.objetos import objetos_bp


app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(objetos_bp)
if __name__ == '__main__':
    app.run(debug=True)

