from django.urls import path

from .views import HomeView

urlpatterns = [
        path('test/', HomeView, name='test'),

]
