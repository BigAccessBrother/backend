from django.urls import path

from project.api.user.view import UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='new_standards'),
]
