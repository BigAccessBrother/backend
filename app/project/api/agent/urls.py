from django.urls import path

from project.api.agent.views import ListAllAgents, AgentDeleteView, \
        AgentRegisterView, AgentActivateView, AgenInstallerDownloadView

urlpatterns = [
        path('', ListAllAgents.as_view(), name='list_all_agents'),
        path('<int:pk>/delete/', AgentDeleteView.as_view(), name='delete_agent'),
        path('<int:pk>/activate/', AgentActivateView.as_view(), name='activate_agent'),
        path('register/', AgentRegisterView.as_view(), name='register_agent'),
        path('installer/', AgenInstallerDownloadView.as_view(), name='download-installer'),
]
