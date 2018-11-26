from django.urls import path

from project.api.user.view import UserListView, UserDeleteView, UserUpdateView

urlpatterns = [
    path('', UserListView.as_view(), name='list_users'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
]
