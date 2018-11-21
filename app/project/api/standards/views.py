from rest_framework.generics import ListAPIView

from project.api.models import SecurityStandard
from project.api.standards.serializer import StandardSerializer


class ListStandardsView(ListAPIView):
    queryset = SecurityStandard.objects.all()
    serializer_class = StandardSerializer
