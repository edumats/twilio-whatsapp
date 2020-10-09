import os
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import emoji

from .models import Appointment, Customer, Mechanic, Message
from .sms import send_sms
from .forms import ReschedulingForm, CreateAppointment, CreateUser, CreateMechanic, CustomerServiceForm, ChangeApppointmentStatus
from .gmail import send_gmail
from .whatsapp import send_whatsapp

def schedule(request):
    if request.method == 'POST':
        # Populate Customer object if customer exists, otherwise populate with POST data
        try:
            customer_phone = request.POST.get('phone_number', 'no phone')
            customer = Customer.objects.get(phone_number=customer_phone)
            customer_form = CreateUser(request.POST, instance=customer)
        except Customer.DoesNotExist:
            customer_form = CreateUser(request.POST)
        # Populate Mechanic if exists, otherwise populate with POST data
        try:
            mechanic_name = request.POST.get('name_mechanic', 'no mechanic')
            mechanic = Mechanic.objects.get(name_mechanic=mechanic_name)
            mechanic_form = CreateMechanic(request.POST, instance=mechanic)
        except Mechanic.DoesNotExist:
            mechanic_form = CreateMechanic(request.POST)

        appointment_form = CreateAppointment(request.POST)

        if appointment_form.is_valid() and customer_form.is_valid() and mechanic_form.is_valid():
            new_customer = customer_form.save()
            new_mechanic = mechanic_form.save()
            appointment_datetime =  appointment_form.cleaned_data['date_scheduled']
            # Format data to a Brazilian standard
            readable_date = appointment_datetime.strftime('%d/%m/%Y %H:%M')
            service_type = appointment_form.cleaned_data['type']
            # Create new appointment
            new_appointment = Appointment.objects.create(
                customer=new_customer,
                mechanic=new_mechanic,
                date_scheduled=appointment_datetime,
                type=service_type
            )
            # new_appointment.save()
            customer_name = customer_form.cleaned_data['name']
            customer_address = customer_form.cleaned_data['address']
            mechanic_name = mechanic_form.cleaned_data['name_mechanic']
            # custom_link = f'http://72c9833bc4d5.ngrok.io/reschedule/{new_appointment.id}'
            custom_link = new_appointment.get_reschedule_url()
            service_type = 'revisão'
            message = f'Olá, {customer_name}. Aqui é o robô do Bike123. O serviço de {service_type} será realizado em {readable_date} no endereço {customer_address} pelo mecânico {mechanic_name}. Caso não possa receber o mecânico ou as informações estejam incorretas, acesso o link: {custom_link}'

            # Send SMS
            # send_sms(message, customer_phone)
            customer_email = customer_form.cleaned_data['email']
            print(message, customer_email)
            # Send E-mail
            # send_gmail(customer_email, 'Agendamento Bike123', message)
            # customer_phone = customer_form.cleaned_data['phone_number']
            # Send Whatsapp
            # send_whatsapp(message, customer_phone)
            messages.success(request, 'E-mail e whatsapp enviados para o cliente')
            return redirect('schedule')

        context = {
            'appointment_form': appointment_form,
            'customer_form': customer_form,
            'mechanic_form': mechanic_form
        }
        return render(request, 'bot_app/schedule.html', context)
    else:
        # In case of GET request
        context = {
            # 'form': CustomerServiceForm()
            'appointment_form': CreateAppointment(initial={'date_scheduled': datetime.today()}),
            'customer_form': CreateUser(initial={'phone_number': '+55'}),
            'mechanic_form': CreateMechanic(),
        }
        return render(request, 'bot_app/schedule.html', context)


def reschedule(request, id=''):
    if request.method == 'POST':
        form = ReschedulingForm(request.POST)
        if form.is_valid():
            check_id = request.POST.get('customer-id', '')
            issue = request.POST.get('customer_issue', '')
            appointment = Appointment.objects.get(id=check_id)
            custom_link = f'http://72c9833bc4d5.ngrok.io/reschedule/{appointment.id}'

            if issue == 'D':
                # Customer needs to reschedule the appointment day
                appointment.status = 'RE'
                appointment.save()

                message_day = f'O cliente {appointment.customer} precisa remarcar o dia do atendimento {custom_link} marcado para {appointment.date_scheduled} com o mecânico {appointment.mechanic}'
                send_gmail('rafael.tales@bike123.com.br', 'Cliente precisa remarcar o dia', message_day)
            elif issue == 'H':
                # Customer needs to reschedule the appointment hour
                appointment.status = 'RE'
                appointment.save()

                message_time = f'O cliente {appointment.customer} precisa remarcar o horário do atendimento {custom_link} marcado para {appointment.date_scheduled} com o mecânico {appointment.mechanic}'
                send_gmail('rafael.tales@bike123.com.br', 'Cliente precisa remarcar o horário', message_time)
            elif issue == 'E':
                # Customer reports that appointment has wrong information
                appointment.status = 'WI'
                appointment.save()

                message_address = f'O atendimento {custom_link} do cliente {appointment.customer} marcado para {appointment.date_scheduled} com o mecânico {appointment.mechanic} está com o endereço incorreto'
                send_gmail('rafael.tales@bike123.com.br', 'Cliente está com endereço incorreto', message_address)
            # Message to customer after sucessfuly submitting the form
            messages.success(request, 'Obrigado, vamos retornar em breve com o novo agendamento')
            return redirect('reschedule')
        else:
            # If form did not pass validation
            messages.error(request, f'Errors: {appointment_form.errors} {mechanic_form.errors} {customer_form.errors}')
            return render(request, 'bot_app/reschedule.html')
    else:
        # When receiving GET requests
        # Id for identifying the customer
        customer_id = id
        form = ReschedulingForm()
        context = {
            'form':form,
            'customer_id': customer_id
        }
        return render(request, 'bot_app/reschedule.html', context)

@csrf_exempt
def bot(request):
    # For listening to Whatsapp messages sent by Twilio
    if request.method == 'POST':
        # Get Twilio SID from POST data
        twilio_token = request.POST.get('AccountSid', 'No SID')
        # Check if message contains correct Twilio SID
        if twilio_token == os.environ.get('TWILIO_ACCOUNT_SID'):
            # retrieve incoming message from POST request in lowercase
            incoming_msg = request.POST['Body'].lower()
            # Get phone number that sent the message. Comes with 'whatsapp:' in front of number
            from_phone = request.POST.get('From', 'No phone number')

            # create Twilio XML response
            resp = MessagingResponse()
            msg = resp.message()

            responded = False

            if 'ajuda' in incoming_msg or 'oi' in incoming_msg:
                response = emoji.emojize(
                """
*Olá! Sou o assistente virtual do Bike123* \U0001F916

Você pode me dar os seguintes comandos:

:arrow_right: *"agendar":* Reagendar um serviço
:arrow_right: *"checar"*: Consultar situação do meu serviço
:arrow_right: *"avaliar"*: Avalie o Bike123  :white_check_mark:
:arrow_right: *"mensagem"*: Quero falar com alguém do Bike123
                """,
                use_aliases=True
                )
                msg.body(response)
                responded = True

            elif 'agendar' in incoming_msg:
                msg.body('Link para reagendar serviço')
                responded = True
            elif 'checar' in incoming_msg:
                try:
                    get_customer = Customer.objects.get(phone_number=from_phone[9:])
                    appointments = get_customer.appointment_set.filter(status='ST')
                    for appointment in appointments:
                        msg.body(f'{appointment.get_type_display} agendado para {appointment.get_date_scheduled_display} - Mecânico {appointment.mechanic}')
                except Customer.DoesNotExist:
                    msg.body('Você não tem serviços ativos.')
                responded = True
            elif 'avaliar' in incoming_msg:
                response = emoji.emojize('Avalie o nosso serviço através desse link: http://shorturl.at/foxP6  :wink:', use_aliases=True)
                msg.body(response)
                responded = True
            elif 'mensagem' in incoming_msg:
                msg.body('Link para página de contato')
                responded = True

            if not responded:
                try:
                    # Get Customer object by using phone, slice to remove 'whatsapp:'
                    # If a customer if found, save the message
                    get_customer = Customer.objects.get(phone_number=from_phone[9:])
                    save_message = Message.objects.create(
                        message=incoming_msg,
                        customer=get_customer
                    )
                    msg.body('Desculpe, não entendi o que você disse. Envie a mensagem "oi" para a lista de comandos.')
                except Customer.DoesNotExist:
                    # If a customer with the provided nubmer does not exist
                    msg.body('Desculpe, não entendi o que você disse. Envie a mensagem "oi" para a lista de comandos.')

            return HttpResponse(str(resp))
        else:
            # Provided Twilio SID does not match
            return HttpResponse('')


class AppointmentListView(generic.ListView):
    model = Appointment
    ordering = ['-date_initiated']

class AppointmentDetailView(UpdateView):
    fields = ['status']
    template_name_suffix = '_detail'

    def get_object(self):
        return get_object_or_404(Appointment, id=self.kwargs.get('id'))

class CustomerDetailView(generic.DetailView):
    model = Customer
