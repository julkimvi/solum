from .home import home_bp
from .usuarios import usuarios_bp
from .servicios import servicios_bp
from .facturacion import facturacion_bp
from .recordatorios import recordatorios_bp

# Exportar los blueprints para ser usados en main.py
__all__ = ['home_bp', 'usuarios_bp', 'servicios_bp', 'facturacion_bp', 'recordatorios_bp']


# from flask import Blueprint

# home_bp = Blueprint('home', __name__)
# usuarios_bp = Blueprint('usuarios', __name__)
# servicios_bp = Blueprint('servicios', __name__)
# facturacion_bp = Blueprint('facturacion', __name__)
# recordatorios_bp = Blueprint('recordatorios', __name__)
