import os

def send_whatsapp(name, address, date, mechanic):
    # Twilio SandBox Number
    from_whatsapp_number = f'whatsapp:{os.environ.get("TWILIO_NUMBER")}'

    to_whatsapp_number = 'whatsapp:+5511992959818'


    client.messages.create(body=f'Olá {name}. Aqui é o robô do Bike123. O serviço será realizado em {date} no endereço {address} pelo mecânico {mechanic}. Responda caso não possa receber o mecânico nesta data ou se as informações estiverem incorretas.',
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
