from django.urls import path

from .views import ListAllClients

urlpatterns = [
        path('', ListAllClients, name='get_all_clients'),



]
