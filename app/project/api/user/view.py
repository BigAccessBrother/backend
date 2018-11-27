from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.api.permissions import IsAdmin
from project.api.user.serializer import UserSerializer


class ActiveUserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        active_user = self.queryset.filter(id=self.request.user.id)
        return active_user


class UserListView(ListAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save(**serializer.validated_data)
            return Response(UserSerializer(new_user).data)


class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])

    def partial_update(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(**serializer.validated_data)
            return Response(UserSerializer(user).data)
