from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Usuario
from app import db
from datetime import datetime
import os

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

# Ruta para registrar usuarios
@usuarios_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form.get('direccion', '')
        telefono = request.form['telefono']
        fecha = request.form.get('fecha', None)
        descripcion = request.form['descripcion']
        imagen = request.files.get('imagen')

        # Validar la fecha
        if not fecha:
            fecha = datetime.utcnow()
        else:
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
                return redirect(url_for('usuarios.register'))

        if not nombre or not telefono or not descripcion:
            flash("Error: Los campos obligatorios no están completos", "error")
            return redirect(url_for('usuarios.register'))

        imagen_path = None
        if imagen and imagen.filename != '':
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash("Error: Tipo de archivo no permitido.", "error")
                return redirect(url_for('usuarios.register'))

            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(upload_folder, filename)
            imagen.save(imagen_path)

        usuario = Usuario(nombre=nombre, direccion=direccion, telefono=telefono, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
        try:
            db.session.add(usuario)
            db.session.commit()
            flash(f"Usuario {nombre} registrado con éxito.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar el usuario: {str(e)}", "error")

        return redirect(url_for('home_bp.home'))

    return render_template('registrar_usuario.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))

# Ruta para buscar y actualizar usuarios
@usuarios_bp.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        if 'usuario_id' in request.form:
            usuario_id = request.form['usuario_id']
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                return render_template('actualizar_usuario.html', usuario=usuario)
            else:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('usuarios.update_user'))
        elif 'buscar' in request.form:
            buscar = request.form['buscar'].strip()
            usuarios = Usuario.query.filter(
                (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
            ).all()

            if len(usuarios) == 1:
                return render_template('actualizar_usuario.html', usuario=usuarios[0])
            elif len(usuarios) > 1:
                return render_template('seleccionar_usuario.html', usuarios=usuarios, action_url='usuarios.update_user')
            else:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('usuarios.update_user'))

    return render_template('actualizar_usuario.html')

# Ruta para confirmar la actualización del usuario
@usuarios_bp.route('/update_user/confirm', methods=['POST'])
def update_user_confirm():
    usuario_id = request.form.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('usuarios.update_user'))

    usuario.nombre = request.form.get('nombre', usuario.nombre)
    usuario.telefono = request.form.get('telefono', usuario.telefono)
    usuario.direccion = request.form.get('direccion', usuario.direccion)
    usuario.descripcion = request.form.get('descripcion', usuario.descripcion)

    try:
        db.session.commit()
        flash(f"Usuario {usuario.nombre} actualizado con éxito.", "success")
    except Exception as e:
        db.session.rollback()
        if "UNIQUE constraint failed" in str(e):
            flash("El teléfono ingresado ya está registrado con otro usuario.", "error")
        else:
            flash(f"Error al actualizar el usuario: {str(e)}", "error")

    return redirect(url_for('home_bp.home'))


# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from app.models import Usuario
# from app import db
# from datetime import datetime
# import os

# usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

# # Ruta para registrar usuarios
# @usuarios_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         direccion = request.form.get('direccion', '')
#         telefono = request.form['telefono']
#         fecha = request.form.get('fecha', None)
#         descripcion = request.form['descripcion']
#         imagen = request.files.get('imagen')

#         # Validar la fecha
#         if not fecha:
#             fecha = datetime.utcnow()  # Usar la fecha actual si está vacío
#         else:
#             try:
#                 fecha = datetime.strptime(fecha, '%Y-%m-%d')  # Formato esperado
#             except ValueError:
#                 flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
#                 return redirect(url_for('usuarios.register'))

#         # Validaciones simples
#         if not nombre or not telefono or not descripcion:
#             flash("Error: Los campos obligatorios no están completos", "error")
#             return redirect(url_for('usuarios.register'))

#         # Guardar la imagen si fue subida
#         imagen_path = None
#         if imagen and imagen.filename != '':
#             allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
#             if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
#                 flash("Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp).", "error")
#                 return redirect(url_for('usuarios.register'))

#             upload_folder = os.path.join('app', 'static', 'uploads')
#             os.makedirs(upload_folder, exist_ok=True)
#             filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
#             imagen_path = os.path.join(upload_folder, filename)
#             imagen.save(imagen_path)

#         # Guardar en la base de datos
#         usuario = Usuario(nombre=nombre, direccion=direccion, telefono=telefono, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
#         try:
#             db.session.add(usuario)
#             db.session.commit()
#             flash(f"Usuario {nombre} registrado con éxito.", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al registrar el usuario: {str(e)}", "error")

#         return redirect(url_for('home'))

#     return render_template('registrar_usuario.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))

# # Ruta para buscar y actualizar usuarios
# @usuarios_bp.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     if request.method == 'POST':
#         if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
#             usuario_id = request.form['usuario_id']
#             usuario = Usuario.query.get(usuario_id)

#             if usuario:
#                 return render_template('actualizar_usuario.html', usuario=usuario)
#             else:
#                 flash("Usuario no encontrado.", "error")
#                 return redirect(url_for('usuarios.update_user'))
#         elif 'buscar' in request.form:  # Verificar si se realizó una búsqueda
#             buscar = request.form['buscar'].strip()
#             usuarios = Usuario.query.filter(
#                 (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
#             ).all()

#             if len(usuarios) == 1:
#                 return render_template('actualizar_usuario.html', usuario=usuarios[0])
#             elif len(usuarios) > 1:
#                 return render_template('seleccionar_usuario.html', usuarios=usuarios)
#             else:
#                 flash("Usuario no encontrado. Intenta nuevamente.", "error")
#                 return redirect(url_for('usuarios.update_user'))

#     return render_template('actualizar_usuario.html')


# # Ruta para confirmar la actualización del usuario
# @usuarios_bp.route('/update_user/confirm', methods=['POST'])
# def update_user_confirm():
#     usuario_id = request.form.get('usuario_id')
#     usuario = Usuario.query.get(usuario_id)

#     if not usuario:
#         flash("Usuario no encontrado", "error")
#         return redirect(url_for('usuarios.update_user'))

#     # Actualizar campos del usuario
#     usuario.nombre = request.form.get('nombre', usuario.nombre)
#     usuario.telefono = request.form.get('telefono', usuario.telefono)
#     usuario.direccion = request.form.get('direccion', usuario.direccion)
#     usuario.descripcion = request.form.get('descripcion', usuario.descripcion)

#     try:
#         db.session.commit()
#         flash(f"Usuario {usuario.nombre} actualizado con éxito.", "success")
#     except Exception as e:
#         db.session.rollback()
#         if "UNIQUE constraint failed" in str(e):
#             flash("El teléfono ingresado ya está registrado con otro usuario.", "error")
#         else:
#             flash(f"Error al actualizar el usuario: {str(e)}", "error")

#     return redirect(url_for('home_bp.home'))



# from flask import render_template, request, flash, redirect, url_for
# from app.models import Usuario
# from app import db
# from datetime import datetime
# from . import usuarios_bp

# @usuarios_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     # Lógica de registro de usuarios
#     # Copiar desde la ruta `/register` original
#     ...

# @usuarios_bp.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     # Lógica de búsqueda y actualización de usuarios
#     # Copiar desde la ruta `/update_user` original
#     ...

# @usuarios_bp.route('/update_user/confirm', methods=['POST'])
# def update_user_confirm():
#     # Confirmación de la actualización de usuarios
#     # Copiar desde la ruta `/update_user/confirm` original
#     ...
