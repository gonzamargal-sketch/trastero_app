from flask_sqlalchemy import SQLAlchemy

# Creamos la instancia de SQLAlchemy
db = SQLAlchemy()

# Modelo Objeto
class Objeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    ubicacion = db.Column(db.String(100))
    cantidad = db.Column(db.Integer, default=1)
    notas = db.Column(db.Text)

    def __repr__(self):
        return f"<Objeto {self.nombre}>"