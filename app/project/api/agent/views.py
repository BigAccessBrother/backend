from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.agent.serializer import AgentSerializer
from project.api.models import Agent


class ListAllAgents(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentDeleteView(DestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentRegisterView(APIView):

    def post(self, request, **kwargs):
        # check if user exists (should be created when login credential are done)
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound('User does not exist')
        try:
            user.check_password(request.data['password'])
        except Exception:
            raise NotFound(f'Password wrong')
        # if pw correct, agent registered on user is created and gets a name referring to the user
        agent = Agent.objects.create(
            user=user,
            system_serial_number=request.data['system_serial_number'],
            computer_name=f'{user.email} {user.agents.count()+1}th agent',
        )

        self.send_agent_register_email(agent)

        return Response(AgentSerializer(agent).data)

    def send_agent_register_email(self, agent):
        admins = User.objects.filter(is_staff=True)
        message = EmailMessage(
            subject='Agent Registration',
            body=f'User: {agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'
                 f'Computer name: {agent.computer_name} ',
            to=[admin.email for admin in admins],
        )
        message.send()
