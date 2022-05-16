from django.shortcuts import render
from rest_framework import (
    viewsets, 
    mixins,
)
from .models import AuthenticationLogs
from .serializers import AuthenticationLogsSerializer

class AuthenticationLogsViewsets(
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
    ):
    queryset = AuthenticationLogs.objects.all()
    serializer_class = AuthenticationLogsSerializer