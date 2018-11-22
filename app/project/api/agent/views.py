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
        agent = Agent.objects.create(
            user__username=request.data['username'],
            user__password=request.data['password']
        )
        return Response(AgentSerializer(agent).data)
