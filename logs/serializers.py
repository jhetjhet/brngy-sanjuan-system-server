from rest_framework import serializers
from .models import AuthenticationLogs
from brngy_user.serializers import BrngyUserSerializer

class AuthenticationLogsSerializer(serializers.ModelSerializer):
    user = BrngyUserSerializer(many=False)

    class Meta:
        model = AuthenticationLogs
        fields = (
            'user',
            'action',
            'date',
        )