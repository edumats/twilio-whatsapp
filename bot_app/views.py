import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.shortcuts import render

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import emoji

from frontend.sms import send_sms
from bot_app.forms import ReschedulingForm
from frontend.forms import CreateAppointment, CreateUser, CreateMechanic


# class RescheduleView(FormView):
#     template_name = 'reschedule.html'
#     form_class = ReschedulingForm
#     sucess_url = '/thanks/'
#
#     def form_valid(self, form):
#         pass

def reschedule(request):
    if request.method == 'POST':
        form = ReschedulingForm(request.POST)
        if form.is_valid():
            return HttpResponse('thanks')
        else:
            return
    else:
        # Id for identifying the customer
        customer_id = 'custom_id'
        form = ReschedulingForm()
        return render(request, 'bot_app/reschedule.html', {'form':form})

@csrf_exempt
def webhook():
    message = request.POST['Body'].lower()
    customer = request.POST['From']
    print(message)
    print(customer)

@csrf_exempt
def bot(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()
        print(repr(request.POST))
        print(request.POST.values())
        print(request.POST.keys())

        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        responded = False

        if incoming_msg == 'oi':
            response = emoji.emojize("""
*Olá! Sou o robô do Bike123* \U0001F916

Você pode me dar os seguintes comandos:

 :arrow_right: *'agendar':* Agendar uma revisão, montagem ou conserto \U0001F468
 :arrow_right: *'reagendar'*: Marcar uma nova data e horário para um serviço \U0001F4C6
 :arrow_right: *'checar'*: Consultar situação do meu serviço  :question:
 :arrow_right: *'avaliar'*: Avaliar um serviço já realizado  :white_check_mark:

""", use_aliases=True)
            msg.body(response)
            responded = True

        elif incoming_msg == 'agendar':
            msg.body('Você gostaria de agendar revisão, montagem ou conserto? Escreva *"revisão"*,  *"montagem"* ou *"conserto"*')
            responded = True

        elif incoming_msg == 'conserto':
            msg.body('Obrigado, solicite o serviço de conserto através desse link: http://bike123.com.br/Checkout/Index/3')
            responded = True

        elif incoming_msg == 'revisão':
            msg.body('Obrigado, solicite o serviço de conserto através desse link: http://bike123.com.br/Checkout/Index/1')
            responded = True

        elif incoming_msg == 'montagem':
            msg.body('Obrigado, solicite o serviço de conserto através desse link: http://bike123.com.br/Checkout/Index/5')
            responded = True

        elif incoming_msg == 'reagendar':
            msg.body('Serviço reagendado.')
            responded = True
        elif incoming_msg == 'checar':
            msg.body('Você ainda não pediu um serviço.')
            responded = True
        elif incoming_msg == 'avaliar':
            response = emoji.emojize('Avalie o nosso serviço através desse link: http://shorturl.at/foxP6  :wink:', use_aliases=True)
            msg.body(response)
            responded = True

        if not responded:
            msg.body('Desculpe, não consegui entender o que você disse. Envie "oi" para a lista de comandos.')

        return HttpResponse(str(resp))

@csrf_exempt
def add(request):

    # Reads Twilio's SID and Token
    client = Client()

    # Twilio SandBox Number
    from_whatsapp_number = os.environ.get('TWILIO_NUMBER')

    to_whatsapp_number = 'whatsapp:+5511992959818'

    type ='Joji'

    code = '123'

    client.messages.create(body=f'Your {type} code is {code}',
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)

    return HttpResponse('OK')

@csrf_exempt
def sms(request):
    pass
