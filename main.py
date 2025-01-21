from app import create_app

# Crea la aplicación usando create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
print(app.url_map)

# from flask import render_template, request, flash, redirect, url_for, jsonify
# from app import create_app, db
# from app.models import Usuario, Servicio, Factura, DetalleFactura, Recordatorio
# from datetime import datetime
# from utils.generate_pdf import generar_factura_pdf
# from utils.scheduler import scheduler
# import os
# from initialize_db import initialize_database

# from dotenv import load_dotenv
# import os

# load_dotenv()

# # Ahora puedes acceder a las variables de entorno
# secret_key = os.getenv('5AIPSCCkzVk7hgw9ALFQyueMEVURh9Xk')
# twilio_account_sid = os.getenv('AC5118ee4e96335d75e8a2a2247dd3211e')

# # Inicializar la base de datos automáticamente
# # initialize_database()

# # Inicializar la aplicación
# app = create_app()

# # Usar la clave secreta desde la variable de entorno
# app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# # Configuración para guardar imágenes subidas
# UPLOAD_FOLDER = 'app/static/uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Función para validar el tipo de archivo subido
# def is_allowed_file(filename, allowed_extensions=None):
#     if allowed_extensions is None:
#         allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
#                 flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
#                 return redirect(url_for('register'))

#         # Validaciones simples
#         if not nombre or not telefono or not descripcion:
#             flash("Error: Los campos obligatorios no están completos", "error")
#             return redirect(url_for('register'))

#         # Guardar la imagen si fue subida
#         imagen_path = None
#         if imagen and imagen.filename != '':
#             if not is_allowed_file(imagen.filename):
#                 flash("Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp).", "error")
#                 return redirect(url_for('register'))

#             filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
#             imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
# @app.route('/update_user', methods=['GET', 'POST'])
# def update_user():
#     if request.method == 'POST':
#         if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
#             usuario_id = request.form['usuario_id']
#             usuario = Usuario.query.get(usuario_id)

#             if usuario:
#                 return render_template('actualizar_usuario.html', usuario=usuario)
#             else:
#                 flash("Usuario no encontrado.", "error")
#                 return redirect(url_for('update_user'))
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
#                 return redirect(url_for('update_user'))

#     return render_template('actualizar_usuario.html')


# # Ruta para confirmar la actualización del usuario
# @app.route('/update_user/confirm', methods=['POST'])
# def update_user_confirm():
#     usuario_id = request.form.get('usuario_id')
#     usuario = Usuario.query.get(usuario_id)

#     if not usuario:
#         flash("Usuario no encontrado", "error")
#         return redirect(url_for('update_user'))

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

#     return redirect(url_for('home'))


# # Ruta para consultar servicios
# @app.route('/consult_service', methods=['GET', 'POST'])
# def consult_service():
#     if request.method == 'POST':
#         if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
#             usuario_id = request.form['usuario_id']
#             usuario = Usuario.query.get(usuario_id)

#             if usuario:
#                 servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#                 return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
#             else:
#                 flash("Usuario no encontrado.", "error")
#                 return redirect(url_for('consult_service'))
#         elif 'buscar' in request.form:  # Verificar si se realizó una búsqueda
#             buscar = request.form['buscar'].strip()
#             usuarios = Usuario.query.filter(
#                 (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
#             ).all()

#             if len(usuarios) == 1:
#                 usuario = usuarios[0]
#                 servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#                 return render_template('consultar_servicio.html', usuario=usuario, servicios=servicios)
#             elif len(usuarios) > 1:
#                 return render_template('seleccionar_usuario.html', usuarios=usuarios)
#             else:
#                 flash("Usuario no encontrado. Intenta nuevamente.", "error")
#                 return redirect(url_for('consult_service'))

#     return render_template('consultar_servicio.html')



# # Ruta para actualizar servicios
# @app.route('/update_service', methods=['GET', 'POST'])
# def update_service():
#     if request.method == 'POST':
#         if 'usuario_id' in request.form:  # Verificar si se seleccionó un usuario
#             usuario_id = request.form['usuario_id']
#             usuario = Usuario.query.get(usuario_id)

#             if usuario:
#                 servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#                 return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
#             else:
#                 flash("Usuario no encontrado.", "error")
#                 return redirect(url_for('update_service'))
#         elif 'buscar' in request.form:  # Verificar si se realizó una búsqueda
#             buscar = request.form['buscar'].strip()
#             usuarios = Usuario.query.filter(
#                 (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
#             ).all()

#             if len(usuarios) == 1:
#                 usuario = usuarios[0]
#                 servicios = Servicio.query.filter_by(usuario_id=usuario.id).all()
#                 return render_template('actualizar_servicio.html', usuario=usuario, servicios=servicios)
#             elif len(usuarios) > 1:
#                 return render_template('seleccionar_usuario.html', usuarios=usuarios)
#             else:
#                 flash("Usuario no encontrado. Intenta nuevamente.", "error")
#                 return redirect(url_for('update_service'))

#     return render_template('actualizar_servicio.html')

# #Ruta para confirmar actualizacion de servicio

# @app.route('/update_service/confirm', methods=['POST'])
# def update_service_confirm():
#     servicio_id = request.form.get('servicio_id')  # Este campo indica si es una actualización
#     usuario_id = request.form.get('usuario_id')
#     descripcion = request.form.get('descripcion')
#     fecha = request.form.get('fecha')
#     imagen = request.files.get('imagen')

#     # Validar campos obligatorios
#     if not usuario_id or not descripcion:
#         flash("Error: Usuario o descripción no proporcionados.", "error")
#         return redirect(url_for('update_service'))

#     # Convertir la fecha a datetime.date
#     try:
#         fecha = datetime.strptime(fecha, '%Y-%m-%d').date() if fecha else datetime.now().date()
#     except ValueError:
#         flash("Error: Fecha no válida. Formato esperado: YYYY-MM-DD", "error")
#         return redirect(url_for('update_service'))

#     # Verificar si estamos actualizando un servicio existente
#     if servicio_id:
#         servicio = Servicio.query.get(servicio_id)
#         if not servicio:
#             flash("Servicio no encontrado.", "error")
#             return redirect(url_for('update_service'))

#         # Actualizar campos del servicio existente
#         servicio.descripcion = descripcion
#         servicio.fecha = fecha

#         # Actualizar imagen si se proporcionó una nueva
#         if imagen and imagen.filename != '':
#             if not is_allowed_file(imagen.filename):
#                 flash("Error: Tipo de archivo no permitido.", "error")
#                 return redirect(url_for('update_service'))

#             filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
#             imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             imagen.save(imagen_path)
#             servicio.imagen = imagen_path

#         try:
#             db.session.commit()
#             flash("Servicio actualizado con éxito.", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al actualizar el servicio: {str(e)}", "error")
#     else:
#         # Crear un nuevo servicio
#         nuevo_servicio = Servicio(
#             usuario_id=usuario_id,
#             descripcion=descripcion,
#             fecha=fecha  # Aquí ya es un objeto datetime.date
#         )

#         # Guardar la imagen si se proporcionó
#         if imagen and imagen.filename != '':
#             if not is_allowed_file(imagen.filename):
#                 flash("Error: Tipo de archivo no permitido.", "error")
#                 return redirect(url_for('update_service'))

#             filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagen.filename}"
#             imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             imagen.save(imagen_path)
#             nuevo_servicio.imagen = imagen_path

#         try:
#             db.session.add(nuevo_servicio)
#             db.session.commit()
#             flash("Nuevo servicio agregado con éxito.", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al agregar el servicio: {str(e)}", "error")

#     return redirect(url_for('home'))
# # Ruta para buscar usuario (usada por AJAX)
# @app.route('/buscar_usuario', methods=['POST'])
# def buscar_usuario():
#     nombre = request.json.get('nombre', '').strip()
#     telefono = request.json.get('telefono', '').strip()

#     usuario = Usuario.query.filter(
#         (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
#     ).first()

#     if usuario:
#         return jsonify({
#             "id": usuario.id,
#             "nombre": usuario.nombre,
#             "telefono": usuario.telefono
#         })
#     else:
#         return jsonify({"error": "Usuario no encontrado."}), 404
    
# # Ruta para facturación
# @app.route('/facturacion', methods=['GET', 'POST'])
# def facturacion():
#     if request.method == 'POST':
#         # Capturar datos del formulario
#         nombre = request.form.get('nombre').strip()
#         telefono = request.form.get('telefono').strip()
#         descripciones = request.form.getlist('descripcion[]')
#         cantidades = request.form.getlist('cantidad[]')
#         precios = request.form.getlist('precio[]')

#         # Validar que todos los campos estén completos
#         if not nombre or not telefono or not descripciones or not cantidades or not precios:
#             flash("Error: Todos los campos son obligatorios.", "error")
#             return redirect(url_for('facturacion'))

#         try:
#             # Buscar usuario por nombre o teléfono
#             usuario = Usuario.query.filter(
#                 (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
#             ).first()

#             if not usuario:
#                 flash("Error: Usuario no encontrado. Regístrelo primero.", "error")
#                 return redirect(url_for('facturacion'))

#             # Calcular el total de la factura
#             total_factura = sum(int(c) * float(p) for c, p in zip(cantidades, precios))

#             # Crear la factura
#             factura = Factura(usuario_id=usuario.id, total=total_factura)
#             db.session.add(factura)
#             db.session.flush()  # Asegurarse de que factura.id esté disponible

#             # Crear detalles de la factura
#             productos = []
#             for desc, cant, prec in zip(descripciones, cantidades, precios):
#                 total_producto = int(cant) * float(prec)
#                 detalle = DetalleFactura(
#                     factura_id=factura.id,
#                     descripcion=desc.strip(),
#                     cantidad=int(cant),
#                     precio=float(prec),
#                     total=total_producto
#                 )
#                 db.session.add(detalle)

#                 # Preparar producto para el PDF
#                 productos.append({
#                     "descripcion": desc.strip(),
#                     "cantidad": int(cant),
#                     "precio": float(prec),
#                     "total": total_producto
#                 })

#             # Guardar en la base de datos
#             db.session.commit()

#             # Generar el PDF
#             pdf_path = generar_factura_pdf(usuario, productos, total_factura)

#             flash(f"Factura generada correctamente. <a href='/static/facturas/{os.path.basename(pdf_path)}' target='_blank'>Descargar PDF</a>", "success")

#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al generar la factura: {str(e)}", "error")

#         return redirect(url_for('home'))

#     return render_template('facturacion.html')

# # Ruta para FACTURAR
# @app.route('/facturar', methods=['POST'])
# def facturar():
#     nombre = request.form.get('nombre', '').strip()
#     telefono = request.form.get('telefono', '').strip()
#     direccion = request.form.get('direccion', '').strip()  # Dirección específica para la factura
#     descripciones = request.form.getlist('descripcion[]')
#     cantidades = request.form.getlist('cantidad[]')
#     precios = request.form.getlist('precio[]')

#     # Validar que los campos no estén vacíos
#     if not nombre or not telefono or not direccion or not descripciones or not cantidades or not precios:
#         flash("Error: Todos los campos son obligatorios.", "error")
#         return redirect(url_for('facturacion'))

#     try:
#         # Buscar usuario por nombre o teléfono
#         usuario = Usuario.query.filter(
#             (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
#         ).first()

#         if not usuario:
#             flash("Error: Usuario no encontrado. Regístrelo primero.", "error")
#             return redirect(url_for('facturacion'))

#         # Calcular el total de la factura
#         productos = []
#         total_factura = 0

#         for desc, cant, prec in zip(descripciones, cantidades, precios):
#             cantidad = int(cant)
#             precio = float(prec)
#             total = cantidad * precio
#             productos.append({
#                 "descripcion": desc.strip(),
#                 "cantidad": cantidad,
#                 "precio": precio,
#                 "total": total
#             })
#             total_factura += total

#         # Crear la factura en la base de datos
#         factura = Factura(usuario_id=usuario.id, total=total_factura)
#         db.session.add(factura)
#         db.session.flush()  # Asegurar que factura.id esté disponible

#         # Crear los detalles de la factura
#         for producto in productos:
#             detalle = DetalleFactura(
#                 factura_id=factura.id,
#                 descripcion=producto["descripcion"],
#                 cantidad=producto["cantidad"],
#                 precio=producto["precio"],
#                 total=producto["total"]
#             )
#             db.session.add(detalle)

#         db.session.commit()

#         # Generar el PDF de la factura con la dirección ingresada
#         pdf_path = generar_factura_pdf(usuario, direccion, productos, total_factura)

#         flash(f"Factura generada correctamente. <a href='/static/facturas/{os.path.basename(pdf_path)}' target='_blank'>Descargar PDF</a>", "success")

#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error al generar la factura: {str(e)}", "error")
#         print(f"Error: {str(e)}")  # Log del error para depuración

#     return redirect(url_for('home'))


# # Ruta para configurar recordatorios
# @app.route('/recordatorio', methods=['GET', 'POST'])
# def recordatorio():
#     if request.method == 'POST':
#         usuario_id = request.form.get('usuario_id')
#         descripcion = request.form.get('descripcion', '').strip()
#         fecha_envio = request.form.get('fecha_envio')
#         hora_envio = request.form.get('hora_envio')

#         if not usuario_id or not descripcion or not fecha_envio or not hora_envio:
#             flash("Todos los campos son obligatorios.", "error")
#             return redirect(url_for('recordatorio'))

#         try:
#             # Combinar la fecha y la hora para el envío
#             fecha_hora_envio = datetime.strptime(f"{fecha_envio} {hora_envio}", '%Y-%m-%d %H:%M')

#             # Guardar el recordatorio en la base de datos
#             recordatorio = Recordatorio(
#                 usuario_id=usuario_id,
#                 descripcion=descripcion,
#                 fecha_envio=fecha_hora_envio,
#                 enviado=False
#             )
#             db.session.add(recordatorio)
#             db.session.commit()
#             flash("Recordatorio configurado exitosamente.", "success")
#             return redirect(url_for('home'))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error al configurar el recordatorio: {e}", "error")
#             return redirect(url_for('recordatorio'))

#     # Mostrar el formulario inicial con la lista de usuarios
#     usuarios = Usuario.query.all()
#     return render_template('recordatorio_servicio.html', usuarios=usuarios)


# # Ruta para buscar usuarios antes de configurar recordatorio
# @app.route('/buscar_usuario_recordatorio', methods=['POST'])
# def buscar_usuario_recordatorio():
#     buscar = request.form.get('buscar', '').strip()

#     if not buscar:
#         flash("Debe ingresar un nombre o número de teléfono para buscar.", "error")
#         return redirect(url_for('recordatorio'))

#     # Buscar usuarios por nombre o teléfono
#     usuarios = Usuario.query.filter(
#         (Usuario.nombre.ilike(f"%{buscar}%")) | (Usuario.telefono.ilike(f"%{buscar}%"))
#     ).all()

#     if len(usuarios) == 0:
#         flash("No se encontraron usuarios con ese criterio.", "error")
#         return redirect(url_for('recordatorio'))
#     elif len(usuarios) == 1:
#         # Si hay una sola coincidencia, redirigir directamente al formulario
#         return render_template('recordatorio_servicio.html', usuarios=[usuarios[0]])
#     else:
#         # Si hay varias coincidencias, mostrar la selección
#         return render_template('seleccionar_usuario.html', usuarios=usuarios)

# # Punto de entrada principal
# if __name__ == '__main__':
#     app.run(debug=True)

