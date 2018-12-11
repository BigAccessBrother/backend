from rest_framework import serializers

from project.api.models import Agent, AgentResponse
from project.api.response.serializer import ResponseSerializer
from project.api.users.serializer import DisplayUserSerializer


class AgentSerializer(serializers.ModelSerializer):

    user = DisplayUserSerializer(read_only=True)
    latest_response = serializers.SerializerMethodField(read_only=True)

    def get_latest_response(self, agent):
        try:
            latest_response = AgentResponse.objects.filter(agent_id=agent.id).order_by("-date_created")[0]
            return ResponseSerializer(latest_response).data
        except Exception:
            return 'no responses from this agent'

    class Meta:
        model = Agent
        fields = ['id', 'user', 'computer_name', 'last_response_received', 'secure', 'date_created',
                  'system_serial_number', 'is_active', 'latest_response']
        read_only_fields = ['id', 'user', 'date_created', 'last_response_received', 'latest_response']
