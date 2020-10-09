from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

def send_gmail(customer_email, subject, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [customer_email]
    try:
        result = send_mail(subject, message, email_from, recipient_list)
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    return result
