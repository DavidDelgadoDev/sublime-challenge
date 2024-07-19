from rest_framework import serializers
from .models import IndustryType


class IndustryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryType
        fields = ['name']