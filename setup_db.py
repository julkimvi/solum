from app import create_app, db
import os

# Inicializar la aplicación Flask
app = create_app()

# Ruta de la base de datos
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clientes.db')

with app.app_context():
    # Verificar si la base de datos ya existe
    if not os.path.exists(db_path):
        print("Creando la base de datos...")
        db.create_all()  # Crear las tablas definidas en models.py
        print("Base de datos creada exitosamente.")
    else:
        print("La base de datos ya existe. No se realizaron cambios.")
