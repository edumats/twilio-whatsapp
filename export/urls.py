from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.export_appointment_csv, name='export-appointments'),
    path('mechanics/', views.export_mechanics_csv, name='export-mechanics')
]
