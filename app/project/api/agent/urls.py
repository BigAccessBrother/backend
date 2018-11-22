from django.urls import path

from project.api.agent.views import ListAllAgents

urlpatterns = [
        path('', ListAllAgents.as_view(), name='list_all_agents'),

]
