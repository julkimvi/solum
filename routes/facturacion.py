from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Usuario, Factura, DetalleFactura
from app import db
from utils.generate_pdf import generar_factura_pdf
import os

facturacion_bp = Blueprint('facturacion', __name__, template_folder='templates')

# Ruta para facturación
@facturacion_bp.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form.get('nombre').strip()
        telefono = request.form.get('telefono').strip()
        descripciones = request.form.getlist('descripcion[]')
        cantidades = request.form.getlist('cantidad[]')
        precios = request.form.getlist('precio[]')

        # Validar que todos los campos estén completos
        if not nombre or not telefono or not descripciones or not cantidades or not precios:
            flash("Error: Todos los campos son obligatorios.", "error")
            return redirect(url_for('facturacion.facturacion'))

        try:
            # Buscar usuario por nombre o teléfono
            usuario = Usuario.query.filter(
                (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
            ).first()

            if not usuario:
                flash("Error: Usuario no encontrado. Regístrelo primero.", "error")
                return redirect(url_for('facturacion.facturacion'))

            # Calcular el total de la factura
            total_factura = sum(int(c) * float(p) for c, p in zip(cantidades, precios))

            # Crear la factura
            factura = Factura(usuario_id=usuario.id, total=total_factura)
            db.session.add(factura)
            db.session.flush()  # Asegurarse de que factura.id esté disponible

            # Crear detalles de la factura
            productos = []
            for desc, cant, prec in zip(descripciones, cantidades, precios):
                total_producto = int(cant) * float(prec)
                detalle = DetalleFactura(
                    factura_id=factura.id,
                    descripcion=desc.strip(),
                    cantidad=int(cant),
                    precio=float(prec),
                    total=total_producto
                )
                db.session.add(detalle)

                # Preparar producto para el PDF
                productos.append({
                    "descripcion": desc.strip(),
                    "cantidad": int(cant),
                    "precio": float(prec),
                    "total": total_producto
                })

            # Guardar en la base de datos
            db.session.commit()

            # Generar el PDF
            pdf_path = generar_factura_pdf(usuario, productos, total_factura)

            flash(f"Factura generada correctamente. <a href='/static/facturas/{os.path.basename(pdf_path)}' target='_blank'>Descargar PDF</a>", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Error al generar la factura: {str(e)}", "error")

        return redirect(url_for('home_bp.home'))  # Cambiado a 'home_bp.home'

    return render_template('facturacion.html')


# Ruta para generar factura
@facturacion_bp.route('/facturar', methods=['POST'])
def facturar():
    nombre = request.form.get('nombre', '').strip()
    telefono = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()  # Dirección específica para la factura
    descripciones = request.form.getlist('descripcion[]')
    cantidades = request.form.getlist('cantidad[]')
    precios = request.form.getlist('precio[]')

    # Validar que los campos no estén vacíos
    if not nombre or not telefono or not direccion or not descripciones or not cantidades or not precios:
        flash("Error: Todos los campos son obligatorios.", "error")
        return redirect(url_for('facturacion.facturacion'))

    try:
        # Buscar usuario por nombre o teléfono
        usuario = Usuario.query.filter(
            (Usuario.nombre.ilike(f"%{nombre}%")) | (Usuario.telefono.ilike(f"%{telefono}%"))
        ).first()

        if not usuario:
            flash("Error: Usuario no encontrado. Regístrelo primero.", "error")
            return redirect(url_for('facturacion.facturacion'))

        # Calcular el total de la factura
        productos = []
        total_factura = 0

        for desc, cant, prec in zip(descripciones, cantidades, precios):
            cantidad = int(cant)
            precio = float(prec)
            total = cantidad * precio
            productos.append({
                "descripcion": desc.strip(),
                "cantidad": cantidad,
                "precio": precio,
                "total": total
            })
            total_factura += total

        # Crear la factura en la base de datos
        factura = Factura(usuario_id=usuario.id, total=total_factura)
        db.session.add(factura)
        db.session.flush()  # Asegurar que factura.id esté disponible

        # Crear los detalles de la factura
        for producto in productos:
            detalle = DetalleFactura(
                factura_id=factura.id,
                descripcion=producto["descripcion"],
                cantidad=producto["cantidad"],
                precio=producto["precio"],
                total=producto["total"]
            )
            db.session.add(detalle)

        db.session.commit()

        # Generar el PDF de la factura con la dirección ingresada
        pdf_path = generar_factura_pdf(usuario, direccion, productos, total_factura)

        flash(f"Factura generada correctamente. <a href='/static/facturas/{os.path.basename(pdf_path)}' target='_blank'>Descargar PDF</a>", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al generar la factura: {str(e)}", "error")
        print(f"Error: {str(e)}")  # Log del error para depuración

    return redirect(url_for('home_bp.home'))  # Cambiado a 'home_bp.home'
