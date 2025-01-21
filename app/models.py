from datetime import datetime
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False, unique=True)
    direccion = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    imagen = db.Column(db.String(255), nullable=True)

    servicios = db.relationship('Servicio', backref='usuario', lazy=True)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    imagen = db.Column(db.String(255), nullable=True)

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False)
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)

class DetalleFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Recordatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False)
    enviado = db.Column(db.Boolean, default=False)

    usuario = db.relationship('Usuario', backref=db.backref('recordatorios', lazy=True))























# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# # Configuración de la aplicación Flask
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliente.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Inicialización de la base de datos
# db = SQLAlchemy(app)

# # Definición de los modelos
# class Usuario(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100), nullable=False)
#     telefono = db.Column(db.String(15), nullable=False, unique=True)
#     direccion = db.Column(db.String(255), nullable=True)
#     descripcion = db.Column(db.Text, nullable=False)
#     fecha = db.Column(db.DateTime, default=datetime.utcnow)
#     imagen = db.Column(db.String(255), nullable=True)

# class Servicio(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
#     descripcion = db.Column(db.Text, nullable=False)
#     fecha = db.Column(db.DateTime, default=datetime.utcnow)
#     imagen = db.Column(db.String(255), nullable=True)

#     usuario = db.relationship('Usuario', backref=db.backref('servicios', lazy=True))

# # Crear las tablas en la base de datos
# with app.app_context():
#     db.create_all()
#     print("Base de datos 'cliente.db' creada con éxito.")












































