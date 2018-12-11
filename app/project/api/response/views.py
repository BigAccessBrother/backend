from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.models import AgentResponse
from project.api.permissions import HasRegisteredAgent, IsAdmin
from project.api.response.serializer import ResponseSerializer

from project.api.response.response_helper import compare_fn


class GetAgentsResponsesView(GenericAPIView):
    """List all responses of agent with id = agent_id"""
    permission_classes = (IsAdmin, IsAuthenticated)
    serializer_class = ResponseSerializer
    queryset = AgentResponse.objects.all()

    def get(self, request, agent_id, **kwargs):
        try:
            responses = AgentResponse.objects.filter(agent__id=agent_id)
        except AgentResponse.DoesNotExist:
            raise NotFound(f'Agent with the id {agent_id} doesn\'t exist')
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)


class AgentPostsResponseView(GenericAPIView):
    """Accepts response from agent and compare it to security standards"""
    permission_classes = (HasRegisteredAgent, )
    serializer_class = ResponseSerializer
    queryset = AgentResponse.objects.all()

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            agent_response = serializer.save(**serializer.validated_data)
            return Response(compare_fn(agent_response))
