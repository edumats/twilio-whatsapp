import os
from django.http import HttpResponse
from twilio.rest import Client

def send_sms(message, customer_phone):
    # Twilio Number with SMS capability
    TWILIO_SMS_PHONE_NUMBER = os.environ.get("TWILIO_NUMBER")
    # Example +5511992959818
    to_sms_number = f'{customer_phone}'

    client = Client()

    message = client.messages.create(
        body=message,
        from_=TWILIO_SMS_PHONE_NUMBER,
        to=to_sms_number
    )
