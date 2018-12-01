from django.contrib.auth import get_user_model
from project.api.models import Agent, SecurityStandard
from project.api.tests.master_tests import MasterTestWrapper

User = get_user_model()


class ListStandardsTest(MasterTestWrapper.MasterTests):
    endpoint = 'new_standards'
    methods = ['GET']

    def setUp(self):
        super().setUp()
        for i in range(3):
            SecurityStandard.objects.create(
                user=self.other_user,
                computer_name=f'{other_user.email} {i}',
                system_serial_number='007'
            )