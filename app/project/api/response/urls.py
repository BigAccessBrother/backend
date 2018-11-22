from django.urls import path

from project.api.response.views import GetAgentsResponsesView, AgentPostsResponseView

urlpatterns = [
    path('agent/<int:agent_id>/', GetAgentsResponsesView.as_view(), name='get_one_agents_responses'),
    path('', AgentPostsResponseView.as_view(), name='post_response'),
]
