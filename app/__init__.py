from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    # Configuración de la app
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, template_folder=os.path.join(basedir, '../app/templates'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', f"sqlite:///{os.path.join(basedir, '../instance/cliente.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar Blueprints
    from routes.home import home_bp
    from routes.usuarios import usuarios_bp
    from routes.servicios import servicios_bp
    from routes.facturacion import facturacion_bp
    from routes.recordatorios import recordatorios_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(servicios_bp, url_prefix='/servicios')
    app.register_blueprint(facturacion_bp, url_prefix='/facturacion')
    app.register_blueprint(recordatorios_bp, url_prefix='/recordatorios')

    return app


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os

# # Inicialización de SQLAlchemy
# db = SQLAlchemy()

# def create_app():

#     # Configuración de la base de datos con una ruta absoluta
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     # Configuración de la aplicación
#     # app = Flask(__name__, template_folder='../templates')
#     app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
   
#     app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, '../instance/cliente.db')}"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_ECHO'] = True

#     # Inicializar SQLAlchemy
#     db.init_app(app)

#     return app
