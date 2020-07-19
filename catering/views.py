from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from catering.api.serializers import CaterRequestSerializer
from catering.models import CaterRequest


class CateringViewSet(ModelViewSet):
    queryset = CaterRequest.objects.all()

    serializer_class = CaterRequestSerializer()
    permission_classes = (permissions.AllowAny,)

    # pagination_class = pagination.LimitOffsetPagination
