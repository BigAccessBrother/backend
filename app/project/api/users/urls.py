from django.urls import path

from project.api.users.views import UserListCreateView, ActiveUserView, \
    UserUpdateDeleteView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='list_create_users'),
    path('<int:pk>/', UserUpdateDeleteView.as_view(), name='update_user'),
    path('me/', ActiveUserView.as_view(), name='active_user'),
]
