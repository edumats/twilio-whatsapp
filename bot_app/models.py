import uuid

from django.db import models
from .validators import validate_date

# class Address(models.Model):
#     address = models.CharField(max_length=200)
    # city = models.CharField(max_length=50)
    # state = models.CharField(max_length=2)
    # zip_code = models.CharField(max_length=10, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Número de telefone'
    )
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} - {self.phone_number} - {self.email}'

class Customer(Contact):
    address = models.CharField(max_length=200) # Should go to Appointment
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/customer/{self.id}'


class Message(models.Model):
    message = models.TextField(help_text='Mensagem do cliente')
    date_created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text='Mensagem enviada por'
    )

    def __str__(self):
        return self.message


class Mechanic(models.Model):
    name_mechanic = models.CharField(max_length=150, help_text='Nome do mecânico')
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_mechanic

    def get_absolute_url(self):
        return f'/mechanics/{self.id}'

class Appointment(models.Model):
    FINISHED = 'FI'
    STARTED = 'ST'
    RESCHEDULE = 'RE'
    WRONG_INFO = 'WI'

    STATUS_CHOICES = [
        (FINISHED, 'Finalizado'),
        (STARTED, 'Iniciado'),
        (RESCHEDULE, 'Reagendar'),
        (WRONG_INFO, 'Endereço incorreto')
    ]

    NEW_BIKE_BUILD = 'NB'
    EXERCISE_BIKE_BUILD = 'EB'
    EXPERT_TUNEUP = 'ET'
    SELECT_SERVICE = 'SS'
    FLAT_TIRE_NORMAL = 'FN'
    FLAT_TIRE_ELECTRIC = 'FE'

    TYPE_CHOICES = [
        (NEW_BIKE_BUILD, 'Montagem Bike Nova'),
        (EXERCISE_BIKE_BUILD, 'Montagem Bike Ergométrica'),
        (EXPERT_TUNEUP, 'Revisão Expert'),
        (SELECT_SERVICE, 'Serviço Select'),
        (FLAT_TIRE_NORMAL, 'Pneu Furado Bike Não Elétrica'),
        (FLAT_TIRE_ELECTRIC, 'Pneu Furado Bike Elétrica')
    ]
    # add a service type choice field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        help_text='Cliente'
    )
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.SET_NULL,
        null=True,
        help_text='Mecânico responsável'
    )
    type = models.CharField(
        help_text='Tipo de serviço',
        choices=TYPE_CHOICES,
        max_length=2,
        default=SELECT_SERVICE
    )
    date_initiated = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateTimeField(
        help_text='Data da realização do serviço',
        validators=[validate_date]
    )
    status = models.CharField(
        help_text='Status do serviço',
        choices=STATUS_CHOICES,
        max_length=2,
        default=STARTED
    )
    comments = models.TextField(
        help_text='Observações sobre o serviço',
        blank=True
    )

    def __str__(self):
        return f'{self.type} agendado para {self.date_scheduled} - Mecânico {self.mechanic}'


    def get_absolute_url(self):
        return f'/appointments/{self.id}'

    def get_reschedule_url(self):
        return f'/reschedule/{self.id}'
