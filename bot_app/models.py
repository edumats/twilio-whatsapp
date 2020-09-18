import uuid
from django.db import models

# class Address(models.Model):
#     address = models.CharField(max_length=200)
    # city = models.CharField(max_length=50)
    # state = models.CharField(max_length=2)
    # zip_code = models.CharField(max_length=10, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True, help_text='Número de telefone')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.name} - {self.phone_number} - {self.email}'

class Customer(Contact):
    address = models.CharField(max_length=200)

class Mechanic(models.Model):
    name = models.CharField(max_length=150)
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)

class Appointment(models.Model):
    FINISHED = 'FI'
    STARTED = 'ST'
    RESCHEDULE = 'RE'
    WRONG_INFO = 'WI'

    STATUS_CHOICES = [
        (FINISHED, 'Finished'),
        (STARTED, 'Started'),
        (RESCHEDULE, 'Needs rescheduling'),
        (WRONG_INFO, 'Wrong address')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True, help_text='Cliente')
    mechanic = models.OneToOneField(Mechanic, on_delete=models.SET_NULL, null=True, help_text='Mecânico responsável')
    date_initiated = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateTimeField(help_text='Data da realização do serviço')
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default=STARTED)
    comments = models.TextField()

    def __str__(self):
        return f'Status: {self.status} - Initiated:{self.date_initiated}'
