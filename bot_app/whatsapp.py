import os

from twilio.rest import Client

def send_whatsapp(message, customer_phone='+5511992959818'):
    # Twilio SandBox Number
    from_whatsapp_number = f'whatsapp:{os.environ.get("TWILIO_NUMBER")}'
    to_whatsapp_number = f'whatsapp:{customer_phone}'

    service_type = 'Montagem de bicicleta'
    client = Client()

    message = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(message.sid)
