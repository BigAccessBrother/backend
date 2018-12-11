from django.urls import path

from project.api.agent.views import ListAllAgents, AgentDeleteView, \
        AgentRegisterView, AgentActivateView, AgentInstallerDownloadView

urlpatterns = [
        path('', ListAllAgents.as_view(), name='list_all_agents'),
        path('<int:pk>/delete/', AgentDeleteView.as_view(), name='delete_agent'),
        path('<int:pk>/activate/', AgentActivateView.as_view(), name='activate_agent'),
        path('register/', AgentRegisterView.as_view(), name='register_agent'),
        path('installer/', AgentInstallerDownloadView.as_view(), name='download-installer'),
]
