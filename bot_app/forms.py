import datetime

from django import forms
from django.forms import ModelForm

from .models import Appointment, Customer, Mechanic

from tempus_dominus.widgets import DateTimePicker

class ReschedulingForm(forms.Form):
    DIA = 'D'
    HORA = 'H'
    ENDEREÇO = 'E'
    RESCHEDULE = [
        (DIA, 'Não posso receber o mecânico nesse dia'),
        (HORA, 'Não posso receber o mecânico nesse horário, mas posso nesse dia'),
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
