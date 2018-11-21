from django.urls import path

from project.api.standards.views import StandardsView

urlpatterns = [
    path('', StandardsView.as_view(), name='new_standards'),
]