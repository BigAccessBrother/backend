from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django_cron import CronJobBase, Schedule

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
        created=agent.last_response_received,
        sent=False
    )


class CronSendAlerts(CronJobBase):
    RUN_EVERY_MINS = 720  # 720 every 12 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.send_alerts'    # a unique code

    def send_alerts(self):
        admins = User.objects.filter(is_staff=True)
        alerts_to_send = Alert.objects.filter(sent=False)
        all_alerts = []
        for alert in alerts_to_send:
            info_of_alert = alert.content
            all_alerts += info_of_alert
            alert.sent = True

        message = EmailMessage(
            subject='Daily Security Alert',
            body=all_alerts,
            to=[admin.email for admin in admins],
        )
        message.send()


