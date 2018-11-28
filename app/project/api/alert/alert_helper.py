from django.contrib.auth.models import User

from project.api.models import Alert


def create_alert(report, agent):
    admins = User.objects.filter(is_staff=True)
    resume = f'User: {agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'f'Computer name: ' \
             f'{agent.computer_name}\nReport sent by {agent.last_response_received}\n\n'f'Report:\n'
    details = ''
    for key, value in report.items():
        details += key + ' ' + value + '\n'

    Alert.objects.create(
        # target_machine=agent.computer_name,
        subject=f'Endpoint Security Alert for {agent.computer_name}',
        content=f'{resume}{details} \n\n',
        to=[admin.email for admin in admins],
        sent=False
    )

