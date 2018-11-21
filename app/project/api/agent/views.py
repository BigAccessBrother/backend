from rest_framework.generics import ListAPIView

from project.api.agent.serializer import AgentSerializer
from project.api.models import Agent


class ListAllAgents(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
