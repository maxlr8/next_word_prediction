from rest_framework import serializers
from .models import NWP

class NWP_Serializer(serializers.Serializer):
    class Meta:
        model = NWP
        fields = ['sentence']
