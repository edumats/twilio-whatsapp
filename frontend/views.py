import uuid

from django.shortcuts import render
from .forms import CustomerServiceForm
from django.http import HttpResponse
from twilio.rest import Client

from .gmail import send_gmail
from .whatsapp import send_whatsapp
from .sms import send_sms
from bot_app.models import Appointment, Customer, Mechanic

def index(request):
    context = {
        'form': CustomerServiceForm()
    }
    return render(request, 'frontend/index.html', context)

def message_customer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        customer_address = request.POST.get('address', '')
        service_date = request.POST.get('date', '')
        mechanic_name = request.POST.get('name_mechanic', '')

        if customer_name and customer_email and customer_address and service_date and mechanic_name:
            new_customer, created = Customer.objects.get_or_create(
                name=customer_name,
                phone_number=customer_phone,
                email=customer_email,
                address = customer_address
            )
            new_mechanic = Mechanic.objects.create(name=mechanic_name)
            new_appointment = Appointment.objects.create(customer=new_customer, mechanic=new_mechanic, date_scheduled=service_date)
            print(new_appointment.id)

            custom_link = 'https://lilian-library.herokuapp.com/'
            message = f'Olá {customer_name}. Aqui é o robô do Bike123. O serviço será realizado em {service_date} no endereço {customer_address} pelo mecânico {mechanic_name}. Acesse {custom_link} caso não possa receber o mecânico nesta data ou se as informações estiverem incorretas.'
            # send_sms(message, customer_phone)
            # send_gmail(message, customer_email)

            return HttpResponse('SMS e E-mail enviados')
        else:
            return HttpResponse('Some fields are blank or invalid')
