
from fpdf import FPDF
import os
from datetime import datetime
import re

def generar_factura_pdf(usuario, direccion, productos, total_factura):
    """
    Genera un PDF de factura con diseño moderno, sin líneas en la tabla, y con una dirección específica para la factura.

    Args:
        usuario (object): Objeto con los atributos `nombre`, `telefono` y `id`.
        direccion (str): Dirección proporcionada para esta factura.
        productos (list): Lista de diccionarios con los productos (descripcion, cantidad, precio, total).
        total_factura (float): Total de la factura.

    Returns:
        str: Ruta donde se guardó el archivo PDF.
    """
    # Validar entrada
    if not usuario or not productos or total_factura <= 0:
        raise ValueError("Datos insuficientes o inválidos para generar el PDF.")

    try:
        # Configuración inicial del PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Colores
        header_color = (60, 141, 188)  # Azul moderno
        body_color = (245, 245, 245)  # Fondo claro
        text_color = (0, 0, 0)  # Negro para texto

        # Título
        pdf.set_font("Arial", style="B", size=18)
        pdf.set_text_color(*header_color)
        pdf.cell(0, 10, txt="Recibo de Servicio", ln=True, align="C")
        pdf.ln(10)

        # Información del cliente
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, txt=f"Cliente: {usuario.nombre}", ln=True)
        pdf.cell(0, 10, txt=f"Teléfono: {usuario.telefono}", ln=True)
        pdf.cell(0, 10, txt=f"Dirección: {direccion}", ln=True)  # Dirección específica para la factura
        pdf.cell(0, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(10)

        # Encabezado de productos
        pdf.set_fill_color(*header_color)
        pdf.set_text_color(255, 255, 255)  # Texto blanco
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(80, 10, txt="Descripción", ln=False, align="L", fill=True)
        pdf.cell(30, 10, txt="Cantidad", ln=False, align="C", fill=True)
        pdf.cell(40, 10, txt="Precio Unit.", ln=False, align="C", fill=True)
        pdf.cell(40, 10, txt="Total", ln=True, align="C", fill=True)

        # Detalles de productos
        pdf.set_text_color(*text_color)
        pdf.set_fill_color(*body_color)
        pdf.set_font("Arial", size=12)
        alternate_row = True
        for producto in productos:
            pdf.cell(80, 10, txt=producto["descripcion"], ln=False, align="L", fill=alternate_row)
            pdf.cell(30, 10, txt=str(producto["cantidad"]), ln=False, align="C", fill=alternate_row)
            pdf.cell(40, 10, txt=f"${producto['precio']:.2f}", ln=False, align="C", fill=alternate_row)
            pdf.cell(40, 10, txt=f"${producto['total']:.2f}", ln=True, align="C", fill=alternate_row)
            alternate_row = not alternate_row

        pdf.ln(10)

        # Total
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(*header_color)
        pdf.cell(150, 10, txt="TOTAL:", ln=False, align="R")
        pdf.set_text_color(*text_color)
        pdf.cell(40, 10, txt=f"${total_factura:.2f}", ln=True, align="C")

        # Crear nombre seguro para el archivo
        nombre_seguro = re.sub(r'[^a-zA-Z0-9_\-]', '_', usuario.nombre)
        pdf_folder = os.path.join('static', 'facturas')
        os.makedirs(pdf_folder, exist_ok=True)
        pdf_path = os.path.join(pdf_folder, f"factura_{nombre_seguro}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

        # Generar el PDF
        pdf.output(pdf_path)
        return pdf_path

    except Exception as e:
        raise RuntimeError(f"Error al generar el PDF: {str(e)}")



# from fpdf import FPDF
# import os
# from datetime import datetime

# def generar_factura_pdf(usuario, direccion, productos, total_factura):
#     """
#     Genera un PDF de factura con diseño moderno, sin líneas en la tabla, y con una dirección específica para la factura.

#     Args:
#         usuario (object): Objeto con los atributos `nombre`, `telefono` y `id`.
#         direccion (str): Dirección proporcionada para esta factura.
#         productos (list): Lista de diccionarios con los productos (descripcion, cantidad, precio, total).
#         total_factura (float): Total de la factura.

#     Returns:
#         str: Ruta donde se guardó el archivo PDF.
#     """
#     # Configuración inicial del PDF
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Colores
#     header_color = (60, 141, 188)  # Azul moderno
#     body_color = (245, 245, 245)  # Fondo claro
#     text_color = (0, 0, 0)  # Negro para texto

#     # Título
#     pdf.set_font("Arial", style="B", size=18)
#     pdf.set_text_color(*header_color)
#     pdf.cell(0, 10, txt="Recibo de Servicio", ln=True, align="C")
#     pdf.ln(10)

#     # Información del cliente
#     pdf.set_font("Arial", size=12)
#     pdf.set_text_color(*text_color)
#     pdf.cell(0, 10, txt=f"Cliente: {usuario.nombre}", ln=True)
#     pdf.cell(0, 10, txt=f"Teléfono: {usuario.telefono}", ln=True)
#     pdf.cell(0, 10, txt=f"Dirección: {direccion}", ln=True)  # Dirección específica para la factura
#     pdf.cell(0, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(10)

#     # Encabezado de productos
#     pdf.set_fill_color(*header_color)
#     pdf.set_text_color(255, 255, 255)  # Texto blanco
#     pdf.set_font("Arial", style="B", size=12)
#     pdf.cell(80, 10, txt="Descripción", ln=False, align="L", fill=True)
#     pdf.cell(30, 10, txt="Cantidad", ln=False, align="C", fill=True)
#     pdf.cell(40, 10, txt="Precio Unit.", ln=False, align="C", fill=True)
#     pdf.cell(40, 10, txt="Total", ln=True, align="C", fill=True)

#     # Detalles de productos
#     pdf.set_text_color(*text_color)
#     pdf.set_fill_color(*body_color)
#     pdf.set_font("Arial", size=12)
#     alternate_row = True
#     for producto in productos:
#         pdf.cell(80, 10, txt=producto["descripcion"], ln=False, align="L", fill=alternate_row)
#         pdf.cell(30, 10, txt=str(producto["cantidad"]), ln=False, align="C", fill=alternate_row)
#         pdf.cell(40, 10, txt=f"${producto['precio']:.2f}", ln=False, align="C", fill=alternate_row)
#         pdf.cell(40, 10, txt=f"${producto['total']:.2f}", ln=True, align="C", fill=alternate_row)
#         alternate_row = not alternate_row

#     pdf.ln(10)

#     # Total
#     pdf.set_font("Arial", style="B", size=14)
#     pdf.set_text_color(*header_color)
#     pdf.cell(150, 10, txt="TOTAL:", ln=False, align="R")
#     pdf.set_text_color(*text_color)
#     pdf.cell(40, 10, txt=f"${total_factura:.2f}", ln=True, align="C")

#     # Guardar el PDF en la carpeta correspondiente
#     pdf_folder = os.path.join('static', 'facturas')
#     os.makedirs(pdf_folder, exist_ok=True)
#     pdf_path = os.path.join(pdf_folder, f"factura_{usuario.nombre}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

#     # Generar el PDF
#     pdf.output(pdf_path)

#     return pdf_path






















# from fpdf import FPDF
# import os
# from datetime import datetime

# def generar_factura_pdf(usuario, productos, total_factura):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # Título
#     pdf.set_font("Arial", style="B", size=16)
#     pdf.cell(200, 10, txt="Factura de Venta", ln=True, align="C")
#     pdf.ln(10)

#     # Información del cliente
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Cliente: {usuario.nombre}", ln=True, align="L")
#     pdf.cell(200, 10, txt=f"Teléfono: {usuario.telefono}", ln=True, align="L")
#     pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="L")
#     pdf.ln(10)

#     # Tabla de productos
#     pdf.set_font("Arial", style="B", size=12)
#     pdf.cell(80, 10, txt="Descripción", border=1, align="C")
#     pdf.cell(30, 10, txt="Cantidad", border=1, align="C")
#     pdf.cell(40, 10, txt="Precio Unit.", border=1, align="C")
#     pdf.cell(40, 10, txt="Total", border=1, align="C")
#     pdf.ln()

#     pdf.set_font("Arial", size=12)
#     for producto in productos:
#         pdf.cell(80, 10, txt=producto["descripcion"], border=1)
#         pdf.cell(30, 10, txt=str(producto["cantidad"]), border=1, align="C")
#         pdf.cell(40, 10, txt=f"${producto['precio']:.2f}", border=1, align="C")
#         pdf.cell(40, 10, txt=f"${producto['total']:.2f}", border=1, align="C")
#         pdf.ln()

#     # Total
#     pdf.set_font("Arial", style="B", size=12)
#     pdf.cell(150, 10, txt="TOTAL", border=1, align="R")
#     pdf.cell(40, 10, txt=f"${total_factura:.2f}", border=1, align="C")
#     pdf.ln(10)

#     # Guardar PDF
#     pdf_folder = os.path.join('static', 'facturas')
#     os.makedirs(pdf_folder, exist_ok=True)
#     pdf_path = os.path.join(pdf_folder, f"factura_{usuario.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
#     pdf.output(pdf_path)

#     return pdf_path


