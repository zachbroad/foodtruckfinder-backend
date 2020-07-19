from rest_framework.serializers import ModelSerializer

from catering.models import CaterRequest


class CaterRequestSerializer(ModelSerializer):

    class Meta:
        model = CaterRequest
        fields = (
            'name',
            'email',
            'details',
            'truck',

            'when',
            'duration',
        )

