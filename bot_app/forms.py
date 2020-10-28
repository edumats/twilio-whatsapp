import datetime

from django import forms
from django.forms import ModelForm

from .models import Appointment, Customer, Mechanic

from tempus_dominus.widgets import DateTimePicker
from .gmail import send_gmail

class ReschedulingForm(forms.Form):
    DIA = 'D'
    ENDEREÇO = 'E'
    RESCHEDULE = [
        (DIA, 'Alterar dia e horário do serviço'),
        (ENDEREÇO, 'O endereço onde será realizado o serviço está errado')
    ]
    customer_issue = forms.ChoiceField(label='Selecione o motivo para reagendamento', choices=RESCHEDULE, widget=forms.RadioSelect)
    comment = forms.CharField(label='Observações', widget=forms.Textarea, required=False)

class CustomerServiceForm(forms.Form):
    name = forms.CharField(label='Nome do cliente', max_length=200)
    address = forms.CharField(label='Endereço do cliente', max_length=500)
    date = forms.DateTimeField(label='Data atendimento', initial=datetime.date.today)
    phone = forms.IntegerField(label='Telefone do cliente com DDD', initial='+55')
    email = forms.EmailField(label='E-mail do cliente')
    name_mechanic = forms.CharField(label='Nome do mecânico')

class CreateAppointment(ModelForm):
    class Meta:
        model = Appointment
        fields = ['type','date_scheduled', 'comments']
        labels = {
            'type': 'Tipo de serviço',
            'date_scheduled': 'Quando serviço será realizado',
            'comments': 'Observações'
        }
        widgets = {
            'date_scheduled': DateTimePicker(
                options={
                    'useCurrent': True,
                    'collapse': True,
                    'format': 'YYYY-MM-DD HH:mm'
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            )
        }

class ChangeApppointmentStatus(ModelForm):
    model = Appointment
    fields = 'status'

class CreateUser(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            'name': 'Nome do cliente',
            'phone_number': 'Telefone do cliente',
            'address': 'Endereço do cliente'
        }

class CreateMechanic(ModelForm):
    class Meta:
        model = Mechanic
        fields = '__all__'
        labels = {
            'name_mechanic': 'Nome do mecânico'
        }

class ContactForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    mensagem = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        nome_cliente = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        mensagem_cliente = self.cleaned_data['mensagem']
        mensagem = f'Cliente: {nome_cliente}\nE-mail: {email}\nMensagem:\n{mensagem_cliente}'
        send_gmail('rafael.tales@bike123.com.br', f'Mensagem do {nome_cliente}', mensagem)
