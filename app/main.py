from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__, template_folder='../templates')

# Configuración para guardar imágenes subidas
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para la página de inicio
@app.route('/inicio', methods=['GET'])
def inicio():
    return render_template('inicio.html')


# Ruta para la raíz del servidor
@app.route('/')
def home():
    # Renderizar la página de registro
    return render_template('inicio.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))


# Ruta para registrar usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form['nombre']
        direccion = request.form.get('direccion', '')
        telefono = request.form['telefono']
        fecha = request.form.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        descripcion = request.form['descripcion']
        imagen = request.files.get('imagen')

        # Validaciones simples
        if not nombre or not telefono or not descripcion:
            return "Error: Los campos obligatorios no están completos", 400

        # Guardar la imagen si fue subida
        imagen_path = None
        if imagen and imagen.filename != '':
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
            imagen.save(imagen_path)

        # Respuesta de éxito
        return f"Usuario {nombre} registrado con éxito. Imagen: {imagen_path or 'No subida'}"

    # Renderizar la plantilla registrar_usuario.html
    return render_template('registrar_usuario.html', fecha_default=datetime.now().strftime('%Y-%m-%d'))


# Ruta para buscar y actualizar usuarios
@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    # Simular datos de usuarios existentes (puedes reemplazar esto con una base de datos)
    usuarios = [
        {"nombre": "Juan Pérez", "telefono": "123456789", "direccion": "Av. Principal 123"},
        {"nombre": "María López", "telefono": "987654321", "direccion": "Calle Secundaria 456"},
    ]

    if request.method == 'POST':
        buscar = request.form['buscar']
        # Buscar coincidencias por nombre o teléfono
        usuario_encontrado = next((u for u in usuarios if u["telefono"] == buscar or u["nombre"] == buscar), None)

        if usuario_encontrado:
            # Mostrar formulario de actualización con los datos del usuario encontrado
            return render_template('actualizar_usuario.html', usuario_encontrado=usuario_encontrado)
        else:
            # Usuario no encontrado
            return render_template('actualizar_usuario.html', mensaje="Usuario no encontrado")

    # GET: Mostrar solo el formulario de búsqueda
    return render_template('actualizar_usuario.html')

# Ruta para confirmar la actualización del usuario
@app.route('/update_user/confirm', methods=['POST'])
def update_user_confirm():
    # Capturar los nuevos datos enviados por el formulario
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')

    # Aquí puedes actualizar los datos en una base de datos o archivo
    # En este ejemplo, solo mostramos los datos recibidos
    return f"Datos actualizados: Nombre: {nombre or 'Sin cambios'}, Teléfono: {telefono or 'Sin cambios'}, Dirección: {direccion or 'Sin cambios'}"

# Ruta para actualizar servicio
@app.route('/update_service', methods=['GET', 'POST'])
def update_service():
    # Simular datos de usuarios existentes con historial de servicios
    usuarios = [
        {
            "nombre": "Juan Pérez",
            "telefono": "123456789",
            "direccion": "Av. Principal 123",
            "servicios": [
                {"fecha": "2025-01-01", "descripcion": "Reparación de lavadora"},
                {"fecha": "2025-01-03", "descripcion": "Mantenimiento de secadora"}
            ]
        },
        {
            "nombre": "María López",
            "telefono": "987654321",
            "direccion": "Calle Secundaria 456",
            "servicios": [
                {"fecha": "2025-01-02", "descripcion": "Reparación de refrigerador"}
            ]
        }
    ]

    if request.method == 'POST':
        buscar = request.form['buscar']
        # Buscar coincidencias por nombre o teléfono
        usuario_encontrado = next((u for u in usuarios if u["telefono"] == buscar or u["nombre"] == buscar), None)

        if usuario_encontrado:
            # Mostrar formulario para agregar servicio y datos existentes
            return render_template('actualizar_servicio.html', usuario_encontrado=usuario_encontrado)
        else:
            # Usuario no encontrado
            return render_template('actualizar_servicio.html', mensaje="Usuario no encontrado")

    # GET: Mostrar solo el formulario de búsqueda
    return render_template('actualizar_servicio.html')

# Ruta para confirmar actualizacion de servicio
@app.route('/update_service/confirm', methods=['POST'])
def update_service_confirm():
    # Capturar los datos del nuevo servicio
    descripcion = request.form['descripcion']
    fecha = request.form.get('fecha', datetime.now().strftime('%Y-%m-%d'))  # Fecha actual si está vacía
    imagen = request.files.get('imagen')

    # Guardar la imagen si fue subida (simulación)
    imagen_path = None
    if imagen and imagen.filename != '':
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
        imagen.save(imagen_path)

    # Simular acumulación del servicio en la base de datos
    # (aquí solo devolvemos los datos enviados)
    return f"Nuevo servicio agregado: Descripción: {descripcion}, Fecha: {fecha}, Imagen: {imagen_path or 'No subida'}"

# Ruta para consultar servicio
@app.route('/consult_service', methods=['GET', 'POST'])
def consult_service():
    # Simular datos de usuarios con historial de servicios
    usuarios = [
        {
            "nombre": "Juan Pérez",
            "telefono": "123456789",
            "direccion": "Av. Principal 123",
            "servicios": [
                {"fecha": "2025-01-01", "descripcion": "Reparación de lavadora", "imagen": "/static/uploads/lavadora.jpg"},
                {"fecha": "2025-01-03", "descripcion": "Mantenimiento de secadora", "imagen": None},
                {"fecha": "2025-01-05", "descripcion": "Reparación de refrigerador", "imagen": "/static/uploads/refrigerador.jpg"},
                {"fecha": "2025-01-10", "descripcion": "Instalación de horno", "imagen": "/static/uploads/horno.jpg"}
            ]
        },
        {
            "nombre": "María López",
            "telefono": "987654321",
            "direccion": "Calle Secundaria 456",
            "servicios": [
                {"fecha": "2025-01-02", "descripcion": "Reparación de secadora", "imagen": None}
            ]
        }
    ]

    if request.method == 'POST':
        buscar = request.form['buscar']
        # Buscar coincidencias por nombre o teléfono
        usuario_encontrado = next((u for u in usuarios if u["telefono"] == buscar or u["nombre"] == buscar), None)

        if usuario_encontrado:
            # Mostrar los servicios encontrados
            return render_template('consultar_servicio.html', usuario_encontrado=usuario_encontrado)
        else:
            # Usuario no encontrado
            return render_template('consultar_servicio.html', mensaje="Usuario no encontrado")

    # GET: Mostrar solo el formulario de búsqueda
    return render_template('consultar_servicio.html')


@app.route('/consult_service/all', methods=['GET'])
def consult_service_all():
    # Simular datos de usuarios con historial de servicios
    usuarios = [
        {
            "nombre": "Juan Pérez",
            "telefono": "123456789",
            "direccion": "Av. Principal 123",
            "servicios": [
                {"fecha": "2025-01-01", "descripcion": "Reparación de lavadora", "imagen": "/static/uploads/lavadora.jpg"},
                {"fecha": "2025-01-03", "descripcion": "Mantenimiento de secadora", "imagen": None},
                {"fecha": "2025-01-05", "descripcion": "Reparación de refrigerador", "imagen": "/static/uploads/refrigerador.jpg"},
                {"fecha": "2025-01-10", "descripcion": "Instalación de horno", "imagen": "/static/uploads/horno.jpg"}
            ]
        }
    ]

    telefono = request.args.get('usuario')
    usuario_encontrado = next((u for u in usuarios if u["telefono"] == telefono), None)

    if usuario_encontrado:
        return render_template('consultar_servicio_todos.html', usuario_encontrado=usuario_encontrado)
    else:
        return "Usuario no encontrado", 404

# Ruta para eliminar un servicio
@app.route('/delete_service', methods=['GET', 'POST'])
def delete_service():
    # Simular datos de usuarios con historial de servicios
    usuarios = [
        {
            "nombre": "Juan Pérez",
            "telefono": "123456789",
            "direccion": "Av. Principal 123",
            "servicios": [
                {"fecha": "2025-01-01", "descripcion": "Reparación de lavadora"},
                {"fecha": "2025-01-03", "descripcion": "Mantenimiento de secadora"},
                {"fecha": "2025-01-05", "descripcion": "Reparación de refrigerador"}
            ]
        }
    ]

    if request.method == 'POST':
        # Obtener el índice del servicio a eliminar desde el formulario
        indice = int(request.form['servicio_a_eliminar'])
        telefono = request.args.get('usuario')

        # Buscar el usuario
        usuario_encontrado = next((u for u in usuarios if u["telefono"] == telefono), None)

        if usuario_encontrado:
            # Eliminar el servicio seleccionado
            servicio_eliminado = usuario_encontrado['servicios'].pop(indice)

            # Confirmar eliminación
            return f"Servicio eliminado: {servicio_eliminado['descripcion']} (Fecha: {servicio_eliminado['fecha']})"
        else:
            return "Usuario no encontrado o no tiene servicios registrados.", 404

    # GET: Renderizar la plantilla para eliminar servicio
    telefono = request.args.get('usuario')
    usuario_encontrado = next((u for u in usuarios if u["telefono"] == telefono), None)

    return render_template('eliminar_servicio.html', usuario_encontrado=usuario_encontrado)


if __name__ == '__main__':
    app.run(debug=True)
