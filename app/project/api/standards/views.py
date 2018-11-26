from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.api.models import SecurityStandard
from project.api.permissions import IsAdmin
from project.api.standards.serializer import StandardSerializer


class StandardsView(ListAPIView):
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = SecurityStandard.objects.all()
    serializer_class = StandardSerializer

    def post(self, request, **kwargs):
        serializer = StandardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            standard_list = serializer.save(**serializer.validated_data)
            return Response(StandardSerializer(standard_list).data)
