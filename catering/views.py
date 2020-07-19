from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from catering.api.serializers import CaterRequestSerializer
from catering.models import CaterRequest
from trucks.api.serializers import TruckSerializer
from trucks.models import Truck


class CateringViewSet(ModelViewSet):
    queryset = CaterRequest.objects.all()

    serializer_class = CaterRequestSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return Truck.objects.filter(available_for_catering=True).all()

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return TruckSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            self.permission_classes = (permissions.AllowAny,)
        elif self.action == 'destroy' or self.action == 'update':
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)

        return [permission() for permission in self.permission_classes]
