from django.contrib import admin
from .models import Contact, Customer, Mechanic, Appointment, Message

admin.site.register(Customer)
admin.site.register(Mechanic)
admin.site.register(Appointment)
admin.site.register(Message)
