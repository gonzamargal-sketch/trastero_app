from flask_sqlalchemy import SQLAlchemy
from app import db


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
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "ubicacion": self.ubicacion,
            "notas": self.notas
        }