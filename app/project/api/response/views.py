from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.models import AgentResponse
from project.api.response.serializer import ResponseSerializer


class GetAgentsResponsesView(APIView):

    def get(self, request, agent_id, **kwargs):
        try:
            responses = AgentResponse.objects.filter(agent__id=agent_id)
        except AgentResponse.DoesNotExist:
            raise NotFound(f'Agent with the id {agent_id} doesn\'t exist')
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)
