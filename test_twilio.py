from twilio.rest import Client
import os

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Obtener credenciales de Twilio desde las variables de entorno
twilio_account_sid = os.getenv('AC5118ee4e96335d75e8a2a2247dd3211e')  # SID de tu cuenta
twilio_auth_token = os.getenv('05083306511151f1e28a0604ee3e189b')    # Auth Token
twilio_whatsapp_number = os.getenv('whatsapp:+14155238886')  # Número de WhatsApp de Twilio

# Instanciar el cliente de Twilio
client = Client(twilio_account_sid, twilio_auth_token)

# Número de WhatsApp del destinatario (registrado en el sandbox)
destinatario = 'whatsapp:+50762569184'  # Reemplázalo con tu número de prueba

try:
    # Enviar mensaje de WhatsApp
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número del sandbox de Twilio
        body="¡Recordatorio de prueba desde Twilio!",
        to=destinatario
    )
    print(f"Mensaje enviado con éxito. SID: {message.sid}")
except Exception as e:
    print(f"Error al enviar mensaje: {e}")













#from twilio.rest import Client
# import os

# # Cargar variables de entorno
# from dotenv import load_dotenv
# load_dotenv()

# # Obtener credenciales de Twilio desde las variables de entorno
# twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')  # El SID de tu cuenta
# twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')    # El Auth Token o API Key Secret
# twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')  # Número de WhatsApp de Twilio

# # Instanciar el cliente de Twilio
# client = Client(twilio_account_sid, twilio_auth_token)

# # Número de WhatsApp de prueba
# destinatario = 'whatsapp:+50762569184'  # Reemplázalo con tu número de prueba

# try:
#     # Enviar mensaje de WhatsApp
#     message = client.messages.create(
#         from_=twilio_whatsapp_number,
#         body="¡Hola! Este es un mensaje de prueba desde Twilio.",
#         to=destinatario
#     )
#     print(f"Mensaje enviado con éxito. SID: {message.sid}")
# except Exception as e:
#     print(f"Error al enviar mensaje: {e}")
