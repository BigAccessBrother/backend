from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from project.api.user.serializer import UserSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save(**serializer.validated_data)
            return Response(UserSerializer(new_user).data)
