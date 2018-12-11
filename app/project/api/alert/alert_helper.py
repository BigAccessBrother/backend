from project.api.models import Alert


def create_alert(report, agent):
    """Creates and saves alerts after negative status report"""
    resume = f'User: {agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'f'Computer name: ' \
             f'{agent.computer_name}\nReport sent by {agent.last_response_received}\n\n'f'Report:\n'
    details = ''
    for key, value in report.items():
        details += key + ' ' + value + '\n'

    Alert.objects.create(
        subject=f'Endpoint Security Alert for {agent.computer_name}',
        content=f'{resume}{details} \n\n',
        sent=False
    )
