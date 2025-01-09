from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicialización de SQLAlchemy
db = SQLAlchemy()

def create_app():

    # Configuración de la base de datos con una ruta absoluta
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Configuración de la aplicación
    # app = Flask(__name__, template_folder='../templates')
    app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
   
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, '../instance/cliente.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    # Inicializar SQLAlchemy
    db.init_app(app)

    return app
