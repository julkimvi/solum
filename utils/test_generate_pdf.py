from utils.generate_pdf import generar_factura_pdf

# Crear un objeto de prueba para usuario
class Usuario:
    def __init__(self, id, nombre, telefono):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono

# Crear un usuario de ejemplo
usuario = Usuario(id=1, nombre="Juan Perez", telefono="123456789")

# Lista de productos de prueba
productos = [
    {"descripcion": "Producto 1", "cantidad": 2, "precio": 10.00, "total": 20.00},
    {"descripcion": "Producto 2", "cantidad": 1, "precio": 15.00, "total": 15.00},
]

# Total de la factura
total_factura = 35.00

# Generar PDF
try:
    pdf_path = generar_factura_pdf(usuario, productos, total_factura)
    print(f"PDF generado correctamente en: {pdf_path}")
except Exception as e:
    print(f"Error al generar el PDF: {e}")
