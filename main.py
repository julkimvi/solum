from flask import render_template, request, flash, redirect, url_for
from app import create_app, db
from app.models import Usuario, Servicio
from datetime import datetime
import os
from initialize_db import initialize_database

# Inicializar la base de datos automáticamente
# initialize_database()

# Inicializar la aplicación
app = create_app()

# Usar la clave secreta desde la variable de entorno
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Configuración para guardar imágenes subidas
UPLOAD_FOLDER = 'app/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para validar el tipo de archivo subido
def is_allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('inicio.html')

# Ruta para registrar usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form['nombre']
        direccion = request.form.get('direccion', '')
        telefono = request.form['telefono']
        fecha = request.form.get('fecha', None)
        descripcion = request.form['descripcion']
        imagen = request.files.get('imagen')

        # Validar la fecha
        if not fecha:
            fecha = datetime.utcnow()  # Usar la fecha actual si está vacío
        else:
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d')  # Formato esperado
            except ValueError:
                flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
                return redirect(url_for('register'))

        # Validaciones simples
        if not nombre or not telefono or not descripcion:
            flash("Error: Los campos obligatorios no están completos", "error")
            return redirect(url_for('register'))

        # Guardar la imagen si fue subida
        imagen_path = None
        if imagen and imagen.filename != '':
            if not is_allowed_file(imagen.filename):
                flash("Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp).", "error")
                return redirect(url_for('register'))

            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)

        # Guardar en la base de datos
        usuario = Usuario(nombre=nombre, direccion=direccion, telefono=telefono, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
        try:
            db.session.add(usuario)
            db.session.commit()
            flash(f"Usuario {nombre} registrado con éxito.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar el usuario: {str(e)}", "error")

        return redirect(url_for('home'))

    return render_template('registrar_usuario.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))

# Ruta para buscar y actualizar usuarios
@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        buscar = request.form['buscar'].strip()  # Eliminar espacios adicionales
        # Realizar búsqueda insensible a mayúsculas/minúsculas y permitir parciales
        usuario = Usuario.query.filter(
            (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
        ).first()

        if usuario:
            return render_template('actualizar_usuario.html', usuario=usuario)
        else:
            flash("Usuario no encontrado. Intenta nuevamente.", "error")
            return redirect(url_for('update_user'))

    return render_template('actualizar_usuario.html')



# @app.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             return render_template('actualizar_usuario.html', usuario=usuario)
#         else:
#             flash("Usuario no encontrado", "error")
#             return redirect(url_for('update_user'))

#     return render_template('actualizar_usuario.html')

# Ruta para confirmar la actualización del usuario
@app.route('/update_user/confirm', methods=['POST'])
def update_user_confirm():
    usuario_id = request.form.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('update_user'))

    # Actualizar campos del usuario
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

    return redirect(url_for('update_user'))


# @app.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             return render_template('actualizar_usuario.html', usuario=usuario)
#         else:
#             flash("Usuario no encontrado", "error")
#             return render_template('actualizar_usuario.html')

#     return render_template('actualizar_usuario.html')

# # Ruta para confirmar la actualización del usuario
# @app.route('/update_user/confirm', methods=['POST'])
# def update_user_confirm():
#     usuario_id = request.form['usuario_id']
#     usuario = Usuario.query.get(usuario_id)

#     if usuario:
#         usuario.nombre = request.form.get('nombre', usuario.nombre)
#         usuario.telefono = request.form.get('telefono', usuario.telefono)
#         usuario.direccion = request.form.get('direccion', usuario.direccion)
#         try:
#             db.session.commit()
#             flash(f"Usuario actualizado: {usuario.nombre}", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al actualizar el usuario: {str(e)}", "error")
#     else:
#         flash("Usuario no encontrado", "error")

#     return redirect(url_for('update_user'))

# Ruta para consultar servicios
@app.route('/consult_service', methods=['GET', 'POST'])
def consult_service():
    if request.method == 'POST':
        buscar = request.form['buscar'].strip()  # Eliminar espacios innecesarios

        try:
            # Buscar al usuario por coincidencia parcial en nombre o por teléfono
            usuario = Usuario.query.filter(
                (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
            ).first()

            # Depuración: Verificar si el usuario fue encontrado
            print(f"Usuario encontrado: {usuario}")
            if usuario:
                # Buscar servicios asociados al usuario
                servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()

                # Depuración: Verificar los servicios encontrados
                print(f"Servicios encontrados para el usuario {usuario.id}: {servicios}")

                if not servicios:
                    flash("No se encontraron servicios asociados a este usuario.", "info")

                return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
            else:
                print("No se encontró ningún usuario con el criterio de búsqueda.")
                flash("Usuario no encontrado", "error")
                return render_template('consultar_servicio.html')

        except Exception as e:
            print(f"Error al consultar servicios: {e}")
            flash(f"Error al consultar servicios: {str(e)}", "error")
            return redirect(url_for('home'))

    return render_template('consultar_servicio.html')


# @app.route('/consult_service', methods=['GET', 'POST'])
# def consult_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         try:
#             # Buscar al usuario por nombre o teléfono
#             usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#             # Depuración: Verificar si el usuario fue encontrado
#             print(f"Usuario encontrado: {usuario}")
#             if usuario:
#                 # Buscar servicios asociados al usuario
#                 servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()

#                 # Depuración: Verificar los servicios encontrados
#                 print(f"Servicios encontrados para el usuario {usuario.id}: {servicios}")

#                 if not servicios:
#                     flash("No se encontraron servicios asociados a este usuario.", "info")
#                 return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
#             else:
#                 print("No se encontró ningún usuario con el criterio de búsqueda.")
#                 flash("Usuario no encontrado", "error")
#                 return render_template('consultar_servicio.html')
#         except Exception as e:
#             print(f"Error al consultar servicios: {e}")
#             flash(f"Error al consultar servicios: {str(e)}", "error")
#             return redirect(url_for('home'))

#     return render_template('consultar_servicio.html')




# @app.route('/consult_service', methods=['GET', 'POST'])
# def consult_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#             if not servicios:
#                 flash("No se encontraron servicios asociados a este usuario.", "info")
#             return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
#         else:
#             flash("Usuario no encontrado", "error")
#             return render_template('consultar_servicio.html')

#     return render_template('consultar_servicio.html')

# Ruta para actualizar servicios
@app.route('/update_service', methods=['GET', 'POST'])
def update_service():
    if request.method == 'POST':
        buscar = request.form['buscar'].strip()  # Eliminar espacios extra
        # Realizar búsqueda insensible a mayúsculas/minúsculas
        usuario = Usuario.query.filter(
            (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono == buscar)
        ).first()

        if usuario:
            servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
            return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
        else:
            flash("Usuario no encontrado. Intenta nuevamente.", "error")
            return redirect(url_for('update_service'))

    return render_template('actualizar_servicio.html')

# @app.route('/update_service', methods=['GET', 'POST'])
# def update_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#             return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
#         else:
#             flash("Usuario no encontrado", "error")
#             return redirect(url_for('update_service'))

#     return render_template('actualizar_servicio.html')

# Ruta para confirmar la actualización de un servicio
from datetime import datetime

@app.route('/update_service/confirm', methods=['POST'])
def update_service_confirm():
    servicio_id = request.form.get('servicio_id')  # Este campo indica si es una actualización
    usuario_id = request.form.get('usuario_id')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    imagen = request.files.get('imagen')

    # Validar campos obligatorios
    if not usuario_id or not descripcion:
        flash("Error: Usuario o descripción no proporcionados.", "error")
        return redirect(url_for('update_service'))

    # Convertir la fecha a datetime.date
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date() if fecha else datetime.now().date()
    except ValueError:
        flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
        return redirect(url_for('update_service'))

    # Verificar si estamos actualizando un servicio existente
    if servicio_id:
        servicio = Servicio.query.get(servicio_id)
        if not servicio:
            flash("Servicio no encontrado.", "error")
            return redirect(url_for('update_service'))

        # Actualizar campos del servicio existente
        servicio.descripcion = descripcion
        servicio.fecha = fecha

        # Actualizar imagen si se proporcionó una nueva
        if imagen and imagen.filename != '':
            if not is_allowed_file(imagen.filename):
                flash("Error: Tipo de archivo no permitido.", "error")
                return redirect(url_for('update_service'))

            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            servicio.imagen = imagen_path

        try:
            db.session.commit()
            flash("Servicio actualizado con éxito.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el servicio: {str(e)}", "error")
    else:
        # Crear un nuevo servicio
        nuevo_servicio = Servicio(
            usuario_id=usuario_id,
            descripcion=descripcion,
            fecha=fecha  # Aquí ya es un objeto datetime.date
        )

        # Guardar la imagen si se proporcionó
        if imagen and imagen.filename != '':
            if not is_allowed_file(imagen.filename):
                flash("Error: Tipo de archivo no permitido.", "error")
                return redirect(url_for('update_service'))

            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            nuevo_servicio.imagen = imagen_path

        try:
            db.session.add(nuevo_servicio)
            db.session.commit()
            flash("Nuevo servicio agregado con éxito.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al agregar el servicio: {str(e)}", "error")

    return redirect(url_for('update_service'))




# @app.route('/update_service', methods=['GET', 'POST'])
# def update_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             return render_template('actualizar_servicio.html', usuario=usuario)
#         else:
#             flash("Usuario no encontrado", "error")
#             return render_template('actualizar_servicio.html')

#     return render_template('actualizar_servicio.html')

# # Ruta para confirmar la actualización de un servicio
# @app.route('/update_service/confirm', methods=['POST'])
# def update_service_confirm():
#     usuario_id = request.form['usuario_id']
#     descripcion = request.form['descripcion']
#     fecha = request.form.get('fecha', datetime.now().strftime('%Y-%m-%d'))
#     imagen = request.files.get('imagen')

#     imagen_path = None
#     if imagen and imagen.filename != '':
#         if not is_allowed_file(imagen.filename):
#             flash("Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp).", "error")
#             return redirect(url_for('update_service'))

#         filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
#         imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         imagen.save(imagen_path)

#     servicio = Servicio(usuario_id=usuario_id, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
#     try:
#         db.session.add(servicio)
#         db.session.commit()
#         flash("Nuevo servicio agregado con éxito", "success")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error al agregar el servicio: {str(e)}", "error")

#     return redirect(url_for('update_service'))

# Punto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)













































# from flask import render_template, request
# from app import create_app, db
# from app.models import Usuario, Servicio
# from datetime import datetime
# import os
# from initialize_db import initialize_database

# # Inicializar la base de datos automáticamente
# #verificará y creará las tablas si no existen.
# #initialize_database()


# # Inicializar la aplicación
# app = create_app()

# # Configuración para guardar imágenes subidas
# UPLOAD_FOLDER = 'app/static/uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ruta para la página de inicio
# @app.route('/')
# def home():
#     return render_template('inicio.html')

# # Ruta para registrar usuarios
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Capturar datos del formulario
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
#                 return "Error: Fecha no válida. Formato esperado: YYYY-MM-DD", 400

#         # Validaciones simples
#         if not nombre or not telefono or not descripcion:
#             return "Error: Los campos obligatorios no están completos", 400

#         # Guardar la imagen si fue subida
#         imagen_path = None
#         if imagen and imagen.filename != '':
#             imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
#             imagen.save(imagen_path)

#         # Guardar en la base de datos
#         usuario = Usuario(nombre=nombre, direccion=direccion, telefono=telefono, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
#         db.session.add(usuario)
#         db.session.commit()

#         return f"Usuario {nombre} registrado con éxito. Imagen: {imagen_path or 'No subida'}"

#     return render_template('registrar_usuario.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))


# # Ruta para buscar y actualizar usuarios
# @app.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             return render_template('actualizar_usuario.html', usuario=usuario)
#         else:
#             return render_template('actualizar_usuario.html', mensaje="Usuario no encontrado")

#     return render_template('actualizar_usuario.html')

# # Ruta para confirmar la actualización del usuario
# @app.route('/update_user/confirm', methods=['POST'])
# def update_user_confirm():
#     usuario_id = request.form['usuario_id']
#     usuario = Usuario.query.get(usuario_id)

#     if usuario:
#         usuario.nombre = request.form.get('nombre', usuario.nombre)
#         usuario.telefono = request.form.get('telefono', usuario.telefono)
#         usuario.direccion = request.form.get('direccion', usuario.direccion)
#         db.session.commit()
#         return f"Usuario actualizado: {usuario.nombre}, Teléfono: {usuario.telefono}, Dirección: {usuario.direccion}"
#     else:
#         return "Usuario no encontrado", 404

# # Ruta para consultar servicios
# @app.route('/consult_service', methods=['GET', 'POST'])
# def consult_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#             return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
#         else:
#             return render_template('consultar_servicio.html', mensaje="Usuario no encontrado")

#     return render_template('consultar_servicio.html')

# # Ruta para actualizar servicios
# @app.route('/update_service', methods=['GET', 'POST'])
# def update_service():
#     if request.method == 'POST':
#         buscar = request.form['buscar']
#         usuario = Usuario.query.filter((Usuario.nombre == buscar) | (Usuario.telefono == buscar)).first()

#         if usuario:
#             return render_template('actualizar_servicio.html', usuario=usuario)
#         else:
#             return render_template('actualizar_servicio.html', mensaje="Usuario no encontrado")

#     return render_template('actualizar_servicio.html')

# # Ruta para confirmar la actualización de un servicio
# @app.route('/update_service/confirm', methods=['POST'])
# def update_service_confirm():
#     usuario_id = request.form['usuario_id']
#     descripcion = request.form['descripcion']
#     fecha = request.form.get('fecha', datetime.now().strftime('%Y-%m-%d'))
#     imagen = request.files.get('imagen')

#     imagen_path = None
#     if imagen and imagen.filename != '':
#         imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
#         imagen.save(imagen_path)

#     servicio = Servicio(usuario_id=usuario_id, descripcion=descripcion, fecha=fecha, imagen=imagen_path)
#     db.session.add(servicio)
#     db.session.commit()

#     return f"Nuevo servicio agregado para el usuario con ID {usuario_id}"

# # Punto de entrada principal
# if __name__ == '__main__':
#     app.run(debug=True)
