from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from project.api.models import SecurityStandard
from project.api.standards.serializer import StandardSerializer


# class ListStandardsView(ListAPIView):
#     queryset = SecurityStandard.objects.all()
#     serializer_class = StandardSerializer


class StandardsView(GenericAPIView):

    def get(self, request):
        standard_lists = SecurityStandard.objects.all()
        serializer = StandardSerializer(standard_lists, many=True)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = StandardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            standard_list = serializer.save(**serializer.validated_data)
            return Response(StandardSerializer(standard_list).data)
