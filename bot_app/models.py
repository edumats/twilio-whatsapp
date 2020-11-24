import uuid

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from .validators import validate_date
from .br_state_model import BrazilianState


class CommonUserInfo(models.Model):
    name = models.CharField(max_length=150, help_text='Nome e sobrenome', verbose_name='Nome')
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Número de telefone celular com DDD, somente números. Ex: 11987654321',
        verbose_name='Número telefone'
    )
    email = models.EmailField(unique=True, verbose_name='E-mail')

    class Meta:
        abstract = True


class Customer(CommonUserInfo):
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone_number} - {self.email}'

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk':self.pk})

class Mechanic(CommonUserInfo):
    date_created = models.DateTimeField(auto_now_add=True)
    cpf = models.CharField(
        max_length=11,
        blank=True,
        help_text='CPF, com pontos e traços',
        verbose_name='CPF'
    )
    rg = models.CharField(
        max_length=14,
        blank=True,
        help_text='RG, com pontos e traços',
        verbose_name='RG'
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        help_text='Endereço, com número. Ex: Rua das Rosas, 210',
        verbose_name='Endereço'
    )
    complement = models.CharField(
        max_length=200,
        blank=True,
        help_text='Complemento do endereço, se houver',
        verbose_name='Complemento'
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        help_text='Cidade. Ex: São Paulo',
        verbose_name='Cidade'
    )
    state = models.CharField(
        choices=BrazilianState.choices,
        max_length=2,
        blank=True,
        verbose_name='Estado'
    )
    zip_code = models.CharField(
        max_length=10,
        blank=True,
        help_text='CEP, com traços',
        verbose_name='CEP'
    )
    # Bank account information
    bank = models.CharField(
        max_length=50,
        blank=True,
        help_text='Nome do banco',
        verbose_name='Banco'
    )
    branch = models.CharField(
        max_length=10,
        blank=True,
        help_text='Agência',
        verbose_name='Agência'
    )
    account_number = models.CharField(
        max_length=15,
        help_text='Número da conta, com traços',
        blank=True,
        verbose_name='Número da conta'
    )
    account_owner_name = models.CharField(
        max_length=100,
        help_text='Nome completo do proprietário da conta',
        blank=True,
        verbose_name='Proprietário da conta'
    )
    owner_id = models.CharField(
        max_length=20,
        help_text='CPF ou CNPJ do proprietário da conta',
        blank=True,
        verbose_name='Documento do proprietário'
    )

    def __str__(self):
        return f'{self.name} - {self.city} / {self.state}'

    def get_absolute_url(self):
        return reverse('mechanic-detail', kwargs={'pk': self.pk})


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
    date_created = models.DateTimeField(auto_now_add=True)
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
        help_text='Mecânico responsável pelo serviço'
    )
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=2,
        default=SELECT_SERVICE,
        help_text='Tipo de serviço'
    )
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
    address = models.CharField(
        max_length=200,
        help_text='Endereço onde será realizado o serviço. Ex: Rua das Rosas, 210',
        verbose_name='Endereço do serviço'
    )
    complement = models.CharField(
        max_length=200,
        blank=True,
        help_text='Complemento do endereço, se houver'
    )
    city = models.CharField(max_length=50, help_text='Cidade')
    state = models.CharField(
        choices=BrazilianState.choices,
        max_length=2,
        help_text='Estado'
    )
    zip_code = models.CharField(max_length=10, help_text='CEP, sem traço')
    reference = models.CharField(
        max_length=200,
        blank=True,
        help_text='Referência. Ex: Próximo ao metrô Ana Rosa'
    )
    comments = models.TextField(
        help_text='Observações sobre o serviço',
        blank=True
    )

    def __str__(self):
        return f'{self.type} agendado para {self.date_scheduled} - Mecânico {self.mechanic}'

    def get_absolute_url(self):
        return reverse('appointment-detail', kwargs={'id': self.id})

    def get_reschedule_url(self):
        return reverse('reschedule', kwargs={'id': self. id})


class Review(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.CASCADE,
        help_text='Mecânico que realizou o serviço'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        help_text='Serviço'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text='Nota dada pelo cliente ao serviço'
    )
    comment = models.TextField(blank=True, help_text='Comentário')

    def __str__(self):
        return f'Serviço: {self.appointment} - Nota: {self.rating}'

class Message(models.Model):
    message = models.TextField(help_text='Mensagem do cliente')
    date_created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        help_text='Cliente que enviou a mensagem'
    )

    def __str__(self):
        return self.message
