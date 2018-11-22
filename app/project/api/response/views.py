from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.models import AgentResponse
from project.api.response.serializer import ResponseSerializer

from project.api.response.response_helper import compare_fn


class GetAgentsResponsesView(APIView):

    def get(self, request, agent_id, **kwargs):
        try:
            responses = AgentResponse.objects.filter(agent__id=agent_id)
        except AgentResponse.DoesNotExist:
            raise NotFound(f'Agent with the id {agent_id} doesn\'t exist')
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)


class AgentPostsResponseView(GenericAPIView):
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