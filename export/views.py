import csv
from django.http import HttpResponse
from django.shortcuts import render

from bot_app.models import Appointment, Mechanic

def export_appointment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lista_servicos.csv"'
    appointments = Appointment.objects.all()
    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Criado em',
        'Cliente',
        'Mecânico',
        'Tipo Serviço',
        'Data agendamento',
        'Situação',
        'Endereço',
        'Complemento',
        'Cidade',
        'Estado',
        'CEP',
        'Complemento',
        'Comentários'
    ])
    for appointment in appointments:
        writer.writerow([
            appointment.id,
            appointment.date_created,
            appointment.customer,
            appointment.mechanic,
            appointment.get_type_display(),
            appointment.date_scheduled,
            appointment.get_status_display(),
            appointment.address,
            appointment.complement,
            appointment.city,
            appointment.state,
            appointment.zip_code,
            appointment.complement,
            appointment.comments
        ])
    return response

def export_mechanics_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lista_mecanicos.csv"'
    mechanics = Mechanic.objects.all()
    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Criado em',
        'CPF',
        'RG',
        'Endereço',
        'Complemento',
        'Cidade',
        'Estado',
        'CEP',
        'Banco',
        'Agência',
        'Número da Conta',
        'Proprietário da Conta',
        'Documento Proprietário da Conta'
    ])
    for mechanic in mechanics:
        writer.writerow([
            mechanic.id,
            mechanic.date_created,
            mechanic.cpf,
            mechanic.rg,
            mechanic.address,
            mechanic.complement,
            mechanic.city,
            mechanic.state,
            mechanic.zip_code,
            mechanic.bank,
            mechanic.branch,
            mechanic.account_number,
            mechanic.account_owner_name,
            mechanic.owner_id,
        ])
    return response
