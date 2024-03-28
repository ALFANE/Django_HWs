from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(recipient_list=None):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us.  '
    email_from = settings.EMAIL_HOST_USER
    template = get_template('send_email_test.html')
    user_list = ' '.join(recipient_list)
    send_mail(subject, message, email_from, recipient_list, html_message=template.render(context={
        'recipient_list': user_list,
    }))

