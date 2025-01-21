from twilio.rest import Client
import os

def enviar_mensaje_template(destinatario, content_sid, variables):
    # Configuración desde las variables de entorno
    account_sid = os.getenv('nkjdfjknkdfjnsdkjnfksjdbkjdsbkjd')
    auth_token = os.getenv('dsfjbfkjbsjdfbksjdfbhjdsbfh')
    twilio_whatsapp_number = os.getenv('+1638478085')

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=twilio_whatsapp_number,
            content_sid=content_sid,
            content_variables=variables,
            to=destinatario
        )
        return f"Mensaje enviado con éxito. SID: {message.sid}"
    except Exception as e:
        return f"Error al enviar mensaje: {e}"
