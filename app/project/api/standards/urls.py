from django.urls import path

from project.api.standards.views import ListStandardsView

urlpatterns = [
    path('', ListStandardsView.as_view(), name='standards'),
]