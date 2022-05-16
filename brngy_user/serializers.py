from rest_framework import serializers
from .models import BrngyUser

class BrngyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrngyUser
        fields = (
            'id',
            'username',
        )