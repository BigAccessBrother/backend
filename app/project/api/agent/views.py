from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.agent.agent_helper import name_agent
from project.api.agent.serializer import AgentSerializer
from project.api.models import Agent, AgentInstaller
from project.api.permissions import IsAdmin


class ListAllAgents(ListAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentDeleteView(DestroyAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentActivateView(UpdateAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentRegisterView(APIView):

    def post(self, request, **kwargs):
        # check if user exists
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound('user does not exist')
        try:
            user.check_password(request.data['password'])
        except Exception:
            raise NotFound(f'Password wrong')
        # if pw correct, agent registered on user is created
        agent = Agent.objects.create(
            user=user,
            system_serial_number=request.data['system_serial_number'],
            computer_name=name_agent(user.email, user.agents.count()),
        )
        self.send_agent_register_email(agent)
        return Response(AgentSerializer(agent).data)

    def send_agent_register_email(self, agent):
        admins = User.objects.filter(is_staff=True)
        message = EmailMessage(
            subject='Agent Registration',
            body=f'user: {agent.user}\nSystem Serial Number: {agent.system_serial_number}\n'
                 f'Computer name: {agent.computer_name} ',
            to=[admin.email for admin in admins],
        )
        message.send()


class AgenInstallerDownloadView(GenericAPIView):
    # download agent installer

    def get(self, request, **kwargs):
        # get latest installer
        installer = AgentInstaller.objects.all()[0]
        response = HttpResponse(
            content=installer.file,
            content_type='application/vnd.microsoft.portable-executable',
        )
        response['Content-Disposition'] = f'attachment; filename=' \
            f'"BAB-agent-{installer.os_type}-{installer.version}-setup.exe"'
        return response

    def post(self, request, **kwargs):
        # get latest installer for specified os_type (for future use)
        installer = AgentInstaller.objects.filter(
            os_type__icontains=request.data.get('os_type')
        )[0]
        response = HttpResponse(
            content=installer.file,
            content_type='application/vnd.microsoft.portable-executable',
        )
        response['Content-Disposition'] = f'attachment; filename=' \
            f'"BAB-agent-{installer.os_type}-{installer.version}-setup.exe"'
        return response
