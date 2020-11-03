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
        fields = ['mechanic','type','date_scheduled', 'comments', 'address', 'complement', 'city', 'state', 'zip_code', 'reference']
        labels = {
            'mechanic': 'Mecânico responsável',
            'type': 'Tipo de serviço',
            'date_scheduled': 'Quando serviço será realizado',
            'comments': 'Observações',
            'address': 'Endereço do cliente',
            'complement': 'Complemento',
            'city': 'Cidade',
            'state': 'Estado',
            'zip_code': 'CEP',
            'reference': 'Referência'
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
    class Meta:
        model = Appointment
        fields = ('status',)

class CreateCustomer(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email']
        labels = {
            'name': 'Nome',
            'phone_number': 'Telefone'
        }

class CreateMechanic(ModelForm):
    class Meta:
        model = Mechanic
        fields = '__all__'
        labels = {
            'name': 'Nome',
            'phone_number': 'Telefone',
            'cpf': 'CPF',
            'rg': 'RG',
            'address': 'Endereço',
            'complement': 'Complemento',
            'city': 'Cidade',
            'state': 'Estado',
            'zip_code': 'CEP',
            'bank': 'Banco',
            'branch': 'Agência',
            'account_number': 'Número da conta',
            'account_owner_name': 'Nome do proprietário da conta',
            'owner_id': 'Documento do proprietário da conta'
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
