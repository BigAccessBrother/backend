from django.urls import path

from project.api.agent.views import ListAllAgents, AgentDeleteView

urlpatterns = [
        path('', ListAllAgents.as_view(), name='list_all_agents'),
        path('<int:pk>/delete/', AgentDeleteView.as_view(), name='delete_agent'),
]
