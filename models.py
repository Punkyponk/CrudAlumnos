from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy
db = SQLAlchemy()

# Definición del modelo Alumno
class Alumno(db.Model):
    __tablename__ = 'alumnos'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    carrera = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Alumno {self.nombre}>'

