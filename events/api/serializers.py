from rest_framework import serializers
from events.models import Event
from trucks.api.serializers import TruckSerializer

class EventSerializer(serializers.ModelSerializer):

    trucks = TruckSerializer(many=True)

    class Meta:
        model = Event

        fields = [
            'title',
            'organizer',
            'start_time',
            'end_time',
            'trucks',
            'description'
            ]
    
