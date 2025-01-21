from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Usuario, Recordatorio
from app import db
from datetime import datetime

recordatorios_bp = Blueprint('recordatorios_bp', __name__, template_folder='../app/templates')

@recordatorios_bp.route('/recordatorio', methods=['GET', 'POST'])
def recordatorio():
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        print(f"Usuario seleccionado: {usuario_id}")  # Depuración

        descripcion = request.form.get('descripcion', '').strip()
        fecha_envio = request.form.get('fecha_envio')
        hora_envio = request.form.get('hora_envio')

        if not usuario_id or not descripcion or not fecha_envio or not hora_envio:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('recordatorios_bp.recordatorio'))

        try:
            # Combinar fecha y hora
            fecha_hora_envio = datetime.strptime(f"{fecha_envio} {hora_envio}", '%Y-%m-%d %H:%M')
            recordatorio = Recordatorio(
                usuario_id=usuario_id,
                descripcion=descripcion,
                fecha_envio=fecha_hora_envio,
                enviado=False
            )
            db.session.add(recordatorio)
            db.session.commit()
            flash("Recordatorio configurado exitosamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al configurar el recordatorio: {e}", "error")

        return redirect(url_for('recordatorios_bp.recordatorio'))

    usuarios = Usuario.query.all()
    return render_template('recordatorio_servicio.html', usuarios=usuarios)

@recordatorios_bp.route('/buscar_usuario_recordatorio', methods=['POST'])
def buscar_usuario_recordatorio():
    buscar = request.form.get('buscar', '').strip()

    if not buscar:
        flash("Debe ingresar un nombre o número de teléfono para buscar.", "error")
        return redirect(url_for('recordatorios_bp.recordatorio'))

    usuarios = Usuario.query.filter(
        (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
    ).all()

    print(f"Usuarios encontrados: {[usuario.nombre for usuario in usuarios]}")

    if len(usuarios) == 0:
        flash("No se encontraron usuarios con ese criterio.", "error")
        return redirect(url_for('recordatorios_bp.recordatorio'))
    elif len(usuarios) == 1:
        return render_template('recordatorio_servicio.html', usuarios=[usuarios[0]])
    else:
        return render_template('seleccionar_usuario.html', usuarios=usuarios, action_url='recordatorios_bp.recordatorio')

# from flask import render_template, request, flash, redirect, url_for
# from app.models import Recordatorio, Usuario
# from app import db
# from datetime import datetime
# from . import recordatorios_bp

# @recordatorios_bp.route('/recordatorio', methods=['GET', 'POST'])
# def recordatorio():
#     # Lógica para configurar recordatorios
#     # Copiar desde la ruta `/recordatorio` original
#     ...

# @recordatorios_bp.route('/buscar_usuario_recordatorio', methods=['POST'])
# def buscar_usuario_recordatorio():
#     # Lógica para buscar usuarios antes de configurar recordatorios
#     # Copiar desde la ruta `/buscar_usuario_recordatorio` original
#     ...
