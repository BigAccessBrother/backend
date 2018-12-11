from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.api.permissions import IsAdmin
from project.api.users.serializer import UserSerializer, DisplayUserSerializer


class UserListCreateView(ListCreateAPIView):
    """List / create users"""
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = DisplayUserSerializer


class ActiveUserView(GenericAPIView):
    """Return profile of logged in user"""
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = DisplayUserSerializer

    def get(self, *args, **kwargs):
        return Response(DisplayUserSerializer(self.request.user).data)


class UserUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer
