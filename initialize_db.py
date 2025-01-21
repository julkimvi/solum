from app import create_app, db
from app.models import Usuario, Servicio, Factura, DetalleFactura, Recordatorio

def initialize_database():
    app = create_app()
    with app.app_context():
        # Verifica si las tablas existen y crea las que falten
        try:
            # Intenta crear las tablas
            db.create_all()  # Crea todas las tablas según los modelos definidos
            print("La base de datos y las tablas han sido creadas o ya existían.")
        except Exception as e:
            # Imprime un error si algo falla
            print(f"Error al crear la base de datos: {e}")

if __name__ == "__main__":
    initialize_database()
