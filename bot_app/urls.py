from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot, name='bot'),
    path('add/', views.add, name='add'),
    path('webhook/', views.webhook, name='webhook'),
    path('reschedule/', views.reschedule, name='reschedule'),
]
