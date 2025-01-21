from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models import Usuario, Servicio
from app import db
from datetime import datetime
import os

servicios_bp = Blueprint('servicios', __name__, template_folder='templates')
# Ruta para consultar servicios
@servicios_bp.route('/consult_service', methods=['GET', 'POST'])
def consult_service():
    if request.method == 'POST':
        if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
            usuario_id = request.form['usuario_id']
            usuario = Usuario.query.get(usuario_id)

            if usuario:
                servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
                return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
            else:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('servicios.consult_service'))
        elif 'buscar' in request.form:  # Verificar si se realizó una búsqueda
            buscar = request.form['buscar'].strip()
            usuarios = Usuario.query.filter(
                (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
            ).all()

            if len(usuarios) == 1:
                usuario = usuarios[0]
                servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
                return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
            elif len(usuarios) > 1:
                # Pasar la acción correcta para esta plantilla
                return render_template('seleccionar_usuario.html', usuarios=usuarios, action_url='servicios.consult_service')
            else:
                flash("Usuario no encontrado. Intenta nuevamente.", "error")
                return redirect(url_for('servicios.consult_service'))

    return render_template('consultar_servicio.html')

# Ruta para actualizar servicios
@servicios_bp.route('/update_service', methods=['GET', 'POST'])
def update_service():
    if request.method == 'POST':
        if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
            usuario_id = request.form['usuario_id']
            usuario = Usuario.query.get(usuario_id)

            if usuario:
                servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
                return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
            else:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('servicios.update_service'))
        elif 'buscar' in request.form:  # Verificar si se realizó una búsqueda
            buscar = request.form['buscar'].strip()
            usuarios = Usuario.query.filter(
                (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
            ).all()

            if len(usuarios) == 1:
                usuario = usuarios[0]
                servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
                return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
            elif len(usuarios) > 1:
                # Pasar la acción correcta para esta plantilla
                return render_template('seleccionar_usuario.html', usuarios=usuarios, action_url='servicios.update_service')
            else:
                flash("Usuario no encontrado. Intenta nuevamente.", "error")
                return redirect(url_for('servicios.update_service'))

    return render_template('actualizar_servicio.html')

# Ruta para confirmar actualización de servicio
@servicios_bp.route('/update_service/confirm', methods=['POST'])
def update_service_confirm():
    servicio_id = request.form.get('servicio_id')  # Este campo indica si es una actualización
    usuario_id = request.form.get('usuario_id')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    imagen = request.files.get('imagen')

    # Validar campos obligatorios
    if not usuario_id or not descripcion:
        flash("Error: Usuario o descripción no proporcionados.", "error")
        return redirect(url_for('servicios.update_service'))

    # Convertir la fecha a datetime.date
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date() if fecha else datetime.now().date()
    except ValueError:
        flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
        return redirect(url_for('servicios.update_service'))

    # Verificar si estamos actualizando un servicio existente
    if servicio_id:
        servicio = Servicio.query.get(servicio_id)
        if not servicio:
            flash("Servicio no encontrado.", "error")
            return redirect(url_for('servicios.update_service'))

        # Actualizar campos del servicio existente
        servicio.descripcion = descripcion
        servicio.fecha = fecha

        # Actualizar imagen si se proporcionó una nueva
        if imagen and imagen.filename != '':
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash("Error: Tipo de archivo no permitido.", "error")
                return redirect(url_for('servicios.update_service'))

            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(upload_folder, filename)
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
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash("Error: Tipo de archivo no permitido.", "error")
                return redirect(url_for('servicios.update_service'))

            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
            imagen_path = os.path.join(upload_folder, filename)
            imagen.save(imagen_path)
            nuevo_servicio.imagen = imagen_path

        try:
            db.session.add(nuevo_servicio)
            db.session.commit()
            flash("Nuevo servicio agregado con éxito.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al agregar el servicio: {str(e)}", "error")

    return redirect(url_for('home_bp.home'))


# Ruta para buscar usuario (usada por AJAX)
@servicios_bp.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
    nombre = request.json.get('nombre', '').strip()
    telefono = request.json.get('telefono', '').strip()

    usuario = Usuario.query.filter(
        (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
    ).first()

    if usuario:
        return jsonify({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "telefono": usuario.telefono
        })
    else:
        return jsonify({"error": "Usuario no encontrado."}), 404
