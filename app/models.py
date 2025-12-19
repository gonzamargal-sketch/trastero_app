from flask_sqlalchemy import SQLAlchemy
from app import db


# Modelo Objeto
class Objeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    ubicacion = db.Column(db.String(100))
    cantidad = db.Column(db.Integer, default=1)
    foto = db.Column(db.String(200))

    def __repr__(self):
        return f"<Objeto {self.nombre}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "ubicacion": self.ubicacion,
            "foto": self.foto
        }