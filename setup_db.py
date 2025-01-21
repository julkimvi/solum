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
        print("Actualizando la base de datos...")
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Verifica si las nuevas tablas están creadas, si no, las crea.
        if 'factura' not in tables or 'detalle_factura' not in tables:
            db.create_all()
            print("Nuevas tablas añadidas exitosamente.")
        else:
            print("La base de datos ya contiene todas las tablas necesarias.")
