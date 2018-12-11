from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def name_agent(email, count):
    name = email.split('@')[0]
    return f'{name} #{count + 1}' if count else name


def send_agent_registration_email(agent):
    admins = User.objects.filter(is_staff=True)
    message = EmailMessage(
        subject='Agent Registration',
        body=f'user: {agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'
             f'Computer name: {agent.computer_name} ',
        to=[admin.email for admin in admins],
    )
    message.send()
