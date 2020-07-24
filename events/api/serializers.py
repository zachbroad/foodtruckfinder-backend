from rest_framework import serializers

from events.models import Event
from trucks.api.serializers import TruckSerializer


class EventSerializer(serializers.ModelSerializer):
    trucks = TruckSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Event

        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'trucks',
        ]
