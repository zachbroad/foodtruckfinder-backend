from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from announcements.models import Announcement, AnnouncementImage


class AnnouncementImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AnnouncementImage
        fields = [
            'image',
            'caption',
        ]

    def get_image(self, instance):
        request = self.context.get('request')
        img_url = instance.image.url
        return request.build_absolute_uri(img_url)


class AnnouncementSerializer(ModelSerializer):
    images = AnnouncementImageSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'body',
            'posted_on',
            'edited_on',
            'images',
        ]

