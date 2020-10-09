from django.core.exceptions import ValidationError
from django.utils import timezone

# Checks if provided datetime is not from past datetimes
def validate_date(user_datetime):
    # Uses a timezone aware datetime to be able to compare against user_datetime
    now = timezone.now()
    if now > user_datetime:
        raise ValidationError('Agendamento só pode ser realizado em datas e horários futuros')
