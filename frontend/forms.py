import datetime

from django import forms
from django.forms import ModelForm

from bot_app.models import Appointment, Customer, Mechanic


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
        fields = ['customer', 'mechanic', 'date_scheduled', 'comments']

class CreateUser(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CreateMechanic(ModelForm):
    class Meta:
        model = Mechanic
        fields = '__all__'
