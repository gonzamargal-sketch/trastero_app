from app import create_app, db
from flask import redirect, url_for

app = create_app()


@app.route("/")
def index():
    return redirect(url_for("objetos.inicio"))

if __name__ == "__main__":
    with app.app_context():
        # Crear las tablas si no existen
        db.create_all()
    app.run(debug=True)


