from rest_framework import serializers
from apps.ahorros.models import Movimiento

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'descripcion', 'tipo', 'destino', 'monto', 'alcancia', 'usuario'] #Campos que se reciben y se envian en json
        read_only_fields = ['id','usuario'] # Campos que son solo lectura en el front
        