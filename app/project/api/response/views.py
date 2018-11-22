from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.models import AgentResponse, Agent
from project.api.response.serializer import ResponseSerializer


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

    def post(self, request, **kwargs):

        agent = Agent.objects.get(system_serial_number=request.data['system_serial_number'])
        agents_response = AgentResponse.objects.create(
                                    agent=agent,
                                    agent_version=request.data['agent_version'],
                                    os_type=request.data['os_type'],
                                    os_version=request.data['os_version'],
                                    system_manufacturer=request.data['system_manufacturer'],
                                    system_model=request.data['system_model'],
                                    system_type=request.data['system_type'],
                                    bios_version=request.data['bios_version'],
                                    antispyware_enabled=request.data['antispyware_enabled'],
                                    antispyware_signature_last_updated=request.data
                                    ['antispyware_signature_last_updated'],
                                    antivirus_enabled=request.data['antivirus_enabled'],
                                    antivirus_signature_last_updated=request.data['antivirus_signature_last_updated'],
                                    behavior_monitor_enabled=request.data['behavior_monitor_enabled'],
                                    full_scan_age=request.data['full_scan_age'],
                                    quick_scan_age=request.data['quick_scan_age'],
                                    nis_enabled=request.data['nis_enabled'],
                                    nis_signature_last_updated=request.data['nis_signature_last_updated'],
                                    nis_signature_version=request.data['nis_signature_version'],
                                    on_access_protection_enabled=request.data['on_access_protection_enabled'],
                                    real_time_protection_enabled=request.data['real_time_protection_enabled'],
                                    protection_status=request.data['protection_status'],
                                    )

        return Response(ResponseSerializer(agents_response).data)


