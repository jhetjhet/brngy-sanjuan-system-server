from rest_framework import serializers
from .models import (
    Excel,
)

class ExcelSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Excel
        fields = (
            'id',
            'file',
            'file_name',
            'date_uploaded',
        )
    
    def get_file_name(self, obj):
        return obj.file.name