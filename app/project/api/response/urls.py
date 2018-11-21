from django.urls import path

from project.api.response.views import GetAgentsResponsesView

urlpatterns = [
    path('agent/<int:agent_id>/', GetAgentsResponsesView.as_view(), name='get_one_agents_responses'),
]
