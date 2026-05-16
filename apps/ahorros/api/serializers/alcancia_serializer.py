from rest_framework import serializers
from apps.ahorros.models import Alcancia

class AlcanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alcancia
        fields= ['id','name','fecha_creacion','fecha_objetivo','monto_actual','monto_objetivo','safe_box','activo']
        read_only_fields = ['id','fecha_creacion','safe_box']