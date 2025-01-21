from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__, template_folder='../app/templates')

@home_bp.route('/')
def home():
    return render_template('inicio.html')



# from flask import Blueprint, render_template
# from . import home_bp

# @home_bp.route('/')
# def home():
#     return render_template('inicio.html')
