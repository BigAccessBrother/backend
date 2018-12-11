from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.api.agent.agent_helper import name_agent, \
    send_agent_registration_email
from project.api.agent.serializer import AgentSerializer
from project.api.models import Agent, AgentInstaller
from project.api.permissions import IsAdmin


class ListAllAgents(ListAPIView):
    """List all registered agents"""
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentDeleteView(DestroyAPIView):
    """Delete agent with id pk"""
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentActivateView(UpdateAPIView):
    """Set is_active of agent with id pk to specified bool"""
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentRegisterView(GenericAPIView):
    """Register new agent"""
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def post(self, request, **kwargs):
        # check if endpoint machine already has a registered agent
        if len(Agent.objects.filter(system_serial_number=request.data['system_serial_number'])):
            raise ValueError('machine already has a registered agent')
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound('user does not exist')
        try:
            user.check_password(request.data['password'])
        except Exception:
            raise NotFound('password wrong')
        agent = Agent.objects.create(
            user=user,
            system_serial_number=request.data['system_serial_number'],
            computer_name=name_agent(user.email, user.agents.count()),
        )
        send_agent_registration_email(agent)
        return Response(AgentSerializer(agent).data)


class AgentInstallerDownloadView(GenericAPIView):
    """Download agent installer"""
    permission_classes = (IsAuthenticated, )
    queryset = AgentInstaller.objects.all()
    serializer_class = AgentSerializer

    def get(self, request, **kwargs):
        # get overall latest installer
        installer = AgentInstaller.objects.all()[0]
        response = HttpResponse(
            content=installer.file,
            content_type='application/vnd.microsoft.portable-executable',
        )
        response['Content-Disposition'] = f'attachment; filename=' \
            f'"BAB-agent-{installer.os_type}-{installer.version}-setup.exe"'
        return response

    def post(self, request, **kwargs):
        # get latest installer for specified os_type
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
