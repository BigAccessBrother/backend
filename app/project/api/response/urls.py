from django.urls import path

from project.api.response.views import GetClientsResponsesView

urlpatterns = [
    # all ClientResponses of one client
    path('client/<int:client_id>/', GetClientsResponsesView, name='get_one_clients_responses'),
    # path('client/<int:client_id>/', GetClientsResponsesView.as_view(), name='get_one_clients_responses'),
]