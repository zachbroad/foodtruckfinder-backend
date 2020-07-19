from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from catering.api.serializers import CaterRequestSerializer
from catering.models import CaterRequest


class CateringViewSet(ModelViewSet):
    queryset = CaterRequest.objects.all()

    serializer_class = CaterRequestSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'retrieve' or self.action == 'list':
            return CaterRequest.objects.filter(truck__owner_id=self.request.user).all()

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'update':
            self.permission_classes = (permissions.IsAdminUser,)
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return [permission() for permission in self.permission_classes]
