from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from project.api.models import SecurityStandard
from project.api.permissions import IsAdmin
from project.api.standards.serializer import StandardSerializer


class StandardsView(ListCreateAPIView):
    """List all security standards or create a new one"""
    permission_classes = (IsAdmin, IsAuthenticated)
    queryset = SecurityStandard.objects.all()
    serializer_class = StandardSerializer
