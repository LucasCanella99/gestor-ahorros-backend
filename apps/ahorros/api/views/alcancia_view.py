from rest_framework.viewsets import ModelViewSet
from apps.ahorros.models import Alcancia, SafeBox
from apps.ahorros.api.serializers.alcancia_serializer import AlcanciaSerializer

class AlcanciaViewSet(ModelViewSet):
    serializer_class = AlcanciaSerializer

    def get_queryset(self):
        return Alcancia.objects.filter(safe_box__usuario=self.request.user) # en orm para buscar la relacion en la DB se usa __ aca hace que al crear la alcancia filtre en las safeboxes de la db y la asigne a la safe box asignada(en la db) asignada al usuario que viene de la request
    
    def perform_create(self, serializer):
        safe_box, _ = SafeBox.objects.get_or_create(usuario=self.request.user)
        serializer.save(safe_box=safe_box) # Creamos el puntero de alcancia hacia safebox, no hace falta usuario porque eso ya lo hace el create de safebox