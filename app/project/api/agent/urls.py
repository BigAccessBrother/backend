from django.urls import path

from project.api.agent.views import ListAllAgents, AgentDeleteView, AgentRegisterView

urlpatterns = [
        path('', ListAllAgents.as_view(), name='list_all_agents'),
        path('<int:pk>/delete/', AgentDeleteView.as_view(), name='delete_agent'),
        path('register/', AgentRegisterView.as_view(), name='register_agent'),
]
