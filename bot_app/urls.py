from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('bot/', views.bot, name='bot'),
    path('reschedule/', views.reschedule, name='reschedule'),
    path('reschedule/<uuid:id>/', views.reschedule, name='reschedule'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointments'),
    path('appointments/<uuid:id>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('contact/', views.ContactView.as_view(), name='contato'),
    path('create-mechanic/', views.MechanicCreate.as_view(), name='create-mechanic'),
    path('mechanic/<int:pk>/', views.MechanicDetailView.as_view(), name='mechanic-detail'),
    path('mechanics/', views.MechanicListView.as_view(), name='mechanics'),
    path('update-mechanic/<int:pk>/', views.MechanicUpdate.as_view(), name='update-mechanic'),
]
