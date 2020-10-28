from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('bot/', views.bot, name='bot'),
    path('reschedule/', views.reschedule, name='reschedule'),
    path('reschedule/<uuid:id>/', views.reschedule, name='reschedule'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointments'),
    path('appointments/<uuid:id>', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('customer/<pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('contact/', views.ContactView.as_view(), name='contato')
]
