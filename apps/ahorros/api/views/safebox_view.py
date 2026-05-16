from rest_framework.viewsets import ModelViewSet
from apps.ahorros.models import SafeBox
from apps.ahorros.api.serializers.safebox_serializer import SafeBoxSerializer

class SafeBoxViewSet(ModelViewSet):
    
    serializer_class = SafeBoxSerializer
    
    def get_queryset(self):
        return SafeBox.objects.filter(usuario=self.request.user) 

    def perform_create(self, serializer):
        serializer.save(usuario = self.request.user) # Al crear el objeto python luego de validaciones y todo de create hace que el usuario al crearlo salga unicamente de la consulta