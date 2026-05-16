from rest_framework import serializers
from apps.ahorros.models import SafeBox

class SafeBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeBox
        fields= ['id','usuario','billetera']
        read_only_fields = ['id','usuario']