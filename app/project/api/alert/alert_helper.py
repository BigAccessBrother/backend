from django.contrib.auth.models import User

from project.api.models import Alert


def create_alert(report, agent):
    admins = User.objects.filter(is_staff=True)
    resume = f'Security alert was sent at {agent.last_response_received} by the following endpoint:\n\n'f'User: ' \
             f'{agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'f'Computer name: ' \
             f'{agent.computer_name}\n\n\n'f'Report:\n\n'
    details = ''
    for key, value in report.items():
        details += key + ' ' + value + '\n'

    alert = Alert.objects.create(
        target_machine=agent.computer_name,
        subject=f'Endpoint Security Alert for {agent.computer_name}',
        content=f'{resume}{details}',
        to=[admin.email for admin in admins],
        sent=False
    )

