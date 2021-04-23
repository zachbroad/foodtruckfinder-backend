from django.db.models import QuerySet
from rest_framework import permissions, filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import EventSerializer, ImGoingSerializer
from ..models import Event, ImGoing


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.SearchFilter,)

    @action(detail=True, methods=["POST", "GET", "DELETE", ], permission_classes=[permissions.IsAuthenticated], name="I'm going")
    def going(self, request, pk=None):
        if request.method == "POST":
            obj = ImGoing.objects.create(
                event=self.get_object(),
                user=request.user,
                comments='',
            )

            imgs = ImGoingSerializer(obj)
            return Response(imgs.data, status=status.HTTP_201_CREATED)

        elif request.method == "GET":
            qs: QuerySet = ImGoing.objects.filter(
                event=self.get_object(),
                user=request.user,
            )
            if qs.exists():
                return Response({"going": True}, status=status.HTTP_200_OK)

            return Response({"going": False}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            qs: QuerySet = ImGoing.objects.filter(
                event=self.get_object(),
                user=request.user,
            )
            if qs.exists():
                imgoing: ImGoing = qs.first()
                imgoing.delete()
                return Response({"deleted": True, "message": "You no longer are attending this event."}, status=status.HTTP_200_OK)

            return Response({"deleted": False, "message": "You aren't going to this event!"}, status=status.HTTP_304_NOT_MODIFIED)

        return Response("Invalid method")
