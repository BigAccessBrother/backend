from requests import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.views import APIView

from project.api.agent.serializer import AgentSerializer
from project.api.models import Agent
from project.api.permissions import IsOwnerOrReadOnly


class ListAllAgents(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AgentDeleteView(DestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

