import os
import csv
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import emoji

from .models import Appointment, Customer, Mechanic, Message
from .sms import send_sms
from .forms import ReschedulingForm, CreateAppointment, CreateCustomer, CustomerServiceForm, ChangeApppointmentStatus, ContactForm
from .gmail import send_gmail
from .whatsapp import send_whatsapp

valid_link = 'https://bike123-whatsbot.herokuapp.com'

@login_required
def schedule(request):
    if request.method == 'POST':
        # Populate with a Customer object if customer already exists, otherwise populate with POST data
        try:
            customer_phone = request.POST.get('phone_number', 'no phone')
            customer = Customer.objects.get(phone_number=customer_phone)
            customer_form = CreateCustomer(request.POST, instance=customer)
        except Customer.DoesNotExist:
            customer_form = CreateCustomer(request.POST)

        appointment_form = CreateAppointment(request.POST)

        if appointment_form.is_valid() and customer_form.is_valid():
            new_customer = customer_form.save()
            # Format data to a Brazilian standard

            # Create new appointment
            new_appointment = appointment_form.save()
            new_appointment.customer = new_customer
            new_appointment.save()

            customer_name = customer_form.cleaned_data['name']
            customer_address = appointment_form.cleaned_data['address']
            mechanic_name = new_appointment.mechanic.name
            readable_date = new_appointment.date_scheduled.strftime('%d/%m/%Y %H:%M')
            custom_link = new_appointment.get_reschedule_url()
            service_type = new_appointment.get_type_display()
            message = f'Olá, {customer_name}. Aqui é o assistente virtual do Bike123. Recebemos sua solicitação. Temos um horário disponível para você. O serviço de {service_type} poderá ser  realizado em {readable_date} no endereço {customer_address} pelo mecânico {mechanic_name}. Se você puder nesta data e horário,  não precisa responder e o técnico lhe atenderá conforme combinado. Caso não possa recebê-lo na data sugerida ou se as informações estiverem incorretas, responda para este número escrevendo a mensagem "ajuda".'
            message = f'Olá, {customer_name}. Aqui é o assistente virtual do Bike123. Recebemos sua solicitação. Temos um horário disponível para você. O serviço de {service_type} poderá ser  realizado em {readable_date} no endereço {customer_address} pelo mecânico {mechanic_name}. \nSe você puder nesta data e horário,  não precisa responder e o técnico lhe atenderá conforme combinado.\nCaso não possa recebê-lo na data sugerida ou se as informações estiverem incorretas, responda para este número escrevendo a mensagem "ajuda".'

            # Send SMS
            # send_sms(message, customer_phone)
            customer_email = customer_form.cleaned_data['email']

            # Send E-mail
            send_gmail(customer_email, 'Agendamento Bike123', message)

            # Send Whatsapp
            customer_phone = customer_form.cleaned_data['phone_number']
            send_whatsapp(message, customer_phone)
            messages.success(request, 'E-mail e whatsapp enviados para o cliente')
            return redirect('schedule')

        context = {
            'appointment_form': appointment_form,
            'customer_form': customer_form,
        }
        return render(request, 'bot_app/schedule.html', context)
    else:
        # In case of GET request
        context = {
            # 'form': CustomerServiceForm()
            'appointment_form': CreateAppointment(initial={'date_scheduled': datetime.today()}),
            'customer_form': CreateCustomer(initial={'phone_number': '+55'})
        }
        return render(request, 'bot_app/schedule.html', context)


def reschedule(request, id=''):
    if request.method == 'POST':
        form = ReschedulingForm(request.POST)
        if form.is_valid():
            check_id = request.POST.get('customer-id', '')
            issue = request.POST.get('customer_issue', '')
            appointment = Appointment.objects.get(id=check_id)
            readable_date = appointment.date_scheduled.strftime('%d/%m/%Y %H:%M')
            custom_link = f'{valid_link}/reschedule/{appointment.id}'

            if issue == 'D':
                # Customer needs to reschedule the appointment day
                appointment.status = 'RE'
                appointment.save()

                message_day = f'Cliente {appointment.customer} precisa remarcar o dia do atendimento {custom_link} marcado para {readable_date} com o mecânico {appointment.mechanic}'
                send_gmail('rafael.tales@bike123.com.br', 'Cliente precisa remarcar o dia', message_day)
            elif issue == 'H':
                # Customer needs to reschedule the appointment hour
                appointment.status = 'RE'
                appointment.save()

                message_time = f'O cliente {appointment.customer} precisa remarcar o horário do atendimento {custom_link} marcado para {readable_date} com o mecânico {appointment.mechanic}'
                send_gmail('rafael.tales@bike123.com.br', 'Cliente precisa remarcar o horário', message_time)
            elif issue == 'E':
                # Customer reports that appointment has wrong information
                appointment.status = 'WI'
                appointment.save()

                message_address = f'O atendimento {custom_link} do cliente {appointment.customer} marcado para {readable_date} com o mecânico {appointment.mechanic} está com o endereço incorreto'
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

:arrow_right: *"reagendar":* Reagendar um serviço
:arrow_right: *"checar"*: Consultar situação do meu serviço
:arrow_right: *"avaliar"*: Avalie o Bike123
:arrow_right: *"mensagem"*: Quero falar com alguém do Bike123
                """,
                use_aliases=True
                )
                msg.body(response)
                responded = True

            elif 'reagendar' in incoming_msg:
                try:
                    get_customer = Customer.objects.get(phone_number=from_phone[9:])
                    appointment = get_customer.appointment_set.filter(status='ST').first()
                except Customer.DoesNotExist:
                    msg.body('Você não tem serviços ativos')
                link = f'{valid_link}/reschedule/{appointment.id}'
                msg.body(f'Reagende seu serviço através do link: {link}')
                responded = True
            elif 'checar' in incoming_msg:
                print('checking')
                try:

                    get_customer = Customer.objects.get(phone_number=from_phone[9:])
                    print(f'Checking number: {get_customer.phone_number}')
                    appointments = get_customer.appointment_set.filter(status='ST')
                    for appointment in appointments:
                        date = appointment.date_scheduled.strftime('%d/%m/%Y %H:%M')
                        msg.body(f'{appointment.get_type_display()} agendado para {date} - Mecânico {appointment.mechanic}')
                except Customer.DoesNotExist:
                    print('sem serviços ativos')
                    msg.body('Você não tem serviços ativos.')
                responded = True
            elif 'avaliar' in incoming_msg:
                response = emoji.emojize('Avalie o nosso serviço através desse link: http://shorturl.at/foxP6  :wink:', use_aliases=True)
                msg.body(response)
                responded = True
            elif 'mensagem' in incoming_msg:
                msg.body(f'Entre em contato conosco através do link: {valid_link}/contact')
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

class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    ordering = ['-date_created']

class AppointmentDetailView(LoginRequiredMixin, UpdateView):
    fields = ['status']
    template_name_suffix = '_detail'

    def get_object(self):
        return get_object_or_404(Appointment, id=self.kwargs.get('id'))

class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer

class ContactView(FormView):
    template_name = 'bot_app/contato.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Mensagem enviada! Em breve entraremos em contato')
        return redirect('contato')

class MechanicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mechanic

class MechanicListView(LoginRequiredMixin, generic.ListView):
    model = Mechanic

class MechanicCreate(LoginRequiredMixin, CreateView):
    template_name_suffix = '_create_form'
    model = Mechanic
    fields = '__all__'

class MechanicUpdate(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_update_form'
    model = Mechanic
    fields = '__all__'
