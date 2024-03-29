from rest_framework import serializers

from events.models import Event, ImGoing
from trucks.api.serializers import TruckSerializer


class EventSerializer(serializers.ModelSerializer):
    trucks = TruckSerializer(many=True, required=False, allow_null=True)
    going = serializers.SerializerMethodField()

    class Meta:
        model = Event

        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'trucks',
            'going',
        ]

    def get_going(self, instance):
        return ImGoing.objects.filter(user=self.context['request'].user, event=instance).exists()


class ImGoingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImGoing

        fields = [
            'id',
            'event',
            'user',
            'comments',
        ]
