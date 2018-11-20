from django.urls import path

from .views import HomeView, ListAllClients

urlpatterns = [
        path('test/', HomeView, name='test'),
        path('', ListAllClients, name='get_all_clients'),



]
