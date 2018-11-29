# from django.contrib.auth import get_user_model
# from project.api.models import Agent
# from project.api.tests.master_tests import MasterTestWrapper
#
# User = get_user_model()
#

# class ListAgentsTest(MasterTestWrapper.MasterTests):
#     endpoint = 'list-create-posts'
#     methods = ['GET']
#
#     def setUp(self):
#         super().setUp()
#         for i in range(10):
#             Agent.objects.create(
#                 user=self.other_user,
#                 computer_name=f'{other_user.email} {i}',
#                 system_serial_number='007'
#             )
