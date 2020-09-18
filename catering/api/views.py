from rest_framework import filters
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from catering.api.serializers import CaterRequestSerializer
from catering.models import CaterRequest


class CateringViewSet(ModelViewSet):
    queryset = CaterRequest.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('truck__id',)
    serializer_class = CaterRequestSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return CaterRequest.objects.filter(truck__owner_id=self.request.user).all()
        else:
            return super(CateringViewSet, self).get_queryset()

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'update':
            self.permission_classes = (permissions.IsAdminUser,)
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
