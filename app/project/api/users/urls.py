from django.urls import path

from project.api.users.views import UserListView, UserDeleteView, UserUpdateView, ActiveUserView

urlpatterns = [
    path('', UserListView.as_view(), name='list_users'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('me/', ActiveUserView.as_view(), name='active_user'),
]
