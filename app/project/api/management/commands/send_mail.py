import time
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from project.api.models import Alert


class Command(BaseCommand):
    help = 'Send Mails'

    def handle(self, *args, **options):
        while True:
            time.sleep(30)
            admins = User.objects.filter(is_staff=True)
            alerts_to_send = Alert.objects.filter(sent=False)
            if len(alerts_to_send) > 0:
                all_alerts = ''
                for alert in alerts_to_send:
                    info_of_alert = alert.content
                    all_alerts += info_of_alert + '\n'

                message = EmailMessage(
                    subject='BAB Alerts',
                    body='Current Alerts \n\n' + all_alerts,
                    to=[admin.email for admin in admins],
                )
                message.send()

                for alert in alerts_to_send:
                    alert.sent = True
                    alert.save()
