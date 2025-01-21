from flask import current_app
from app import db, create_app
from app.models import Recordatorio
from twilio.rest import Client
from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler

# Configuración de Twilio
twilio_account_sid = os.getenv('AC5118ee4e96335d75e8a2a2247dd3211e')
twilio_auth_token = os.getenv('05083306511151f1e28a0604ee3e189b')
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Número del sandbox de Twilio

# Inicializar la aplicación Flask
app = create_app()

# Inicializar el scheduler
scheduler = BackgroundScheduler()

def enviar_recordatorios():
    """
    Función para enviar recordatorios pendientes.
    Requiere contexto de aplicación Flask.
    """
    with app.app_context():  # Crear el contexto de aplicación
        try:
            pendientes = Recordatorio.query.filter_by(enviado=False).all()
            for recordatorio in pendientes:
                if recordatorio.fecha_envio <= datetime.now():
                    try:
                        # Enviar mensaje de WhatsApp
                        client = Client(twilio_account_sid, twilio_auth_token)
                        message = client.messages.create(
                            from_=twilio_whatsapp_number,
                            body=f"Recordatorio: {recordatorio.descripcion}",
                            to=f"whatsapp:+{recordatorio.usuario.telefono}"
                        )

                        # Actualizar el estado a enviado
                        recordatorio.enviado = True
                        db.session.commit()

                        # Log de éxito
                        print(f"Recordatorio enviado a {recordatorio.usuario.telefono}: {message.sid}")
                    except Exception as e:
                        # Manejar errores al enviar el mensaje
                        print(f"Error al enviar recordatorio a {recordatorio.usuario.telefono}: {e}")
        except Exception as e:
            # Manejar errores al procesar recordatorios
            print(f"Error al procesar recordatorios: {e}")

# Agregar el trabajo al scheduler
scheduler.add_job(enviar_recordatorios, 'interval', minutes=1)  # Ejecutar cada minuto

# Iniciar el scheduler
scheduler.start()

print("Scheduler iniciado y ejecutándose.")
