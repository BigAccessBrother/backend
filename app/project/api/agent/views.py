from django.contrib.auth.models import User
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
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            raise NotFound('User does not exist')
        try:
            user.check_password(request.data['password'])
        except Exception:
            raise NotFound(f'Password wrong')

        agent = Agent.objects.create(
            user=user,
            system_serial_number=request.data['system_serial_number'],
            computer_name=f'{user.username} {user.agents.count()+1}',
        )
        return Response(AgentSerializer(agent).data)
