from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from apps.ahorros.models import Movimiento, SafeBox, Alcancia
from apps.ahorros.api.serializers.movimiento_serializer import MovimientoSerializer

class MovimientoViewSet(ModelViewSet):
    
    serializer_class = MovimientoSerializer
    
    def get_queryset(self):
        return Movimiento.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        movimiento = serializer.save(usuario=user)
        
        safe_box, _ = SafeBox.objects.get_or_create(usuario=user)
        
        # 1. Ingreso a billetera
        if movimiento.tipo == 'ingreso' and movimiento.destino == 'billetera':
            safe_box.billetera += movimiento.monto
            safe_box.save()
        
        # 2. Ingreso a alcancía
        elif movimiento.tipo == 'ingreso' and movimiento.destino == 'alcancia':
            alcancia = movimiento.alcancia
            if not alcancia or not alcancia.activo:
                raise ValidationError({"error": "No hay una alcancía activa válida"})
            alcancia.monto_actual += movimiento.monto
            alcancia.save()
        
        # 3. Gasto (de billetera, si falta de alcancía activa)
        elif movimiento.tipo == 'gasto':
            billetera = safe_box.billetera
            if billetera >= movimiento.monto:
                safe_box.billetera -= movimiento.monto
                safe_box.save()
            else:
                try:
                    alcancia = Alcancia.objects.get(safe_box=safe_box, activo=True)
                    restante = movimiento.monto - billetera
                    if alcancia.monto_actual >= restante:
                        safe_box.billetera = 0
                        alcancia.monto_actual -= restante
                        safe_box.save()
                        alcancia.save()
                    else:
                        raise ValidationError({"error": "Saldo insuficiente en billetera y alcancía"})
                except Alcancia.DoesNotExist:
                    raise ValidationError({"error": "Saldo insuficiente en billetera y no hay alcancía activa"})
        
        # 4. Ahorrar (transferir de billetera a alcancía activa)
        elif movimiento.tipo == 'ahorrar':
            try:
                alcancia = Alcancia.objects.get(safe_box=safe_box, activo=True)
                if safe_box.billetera >= movimiento.monto:
                    safe_box.billetera -= movimiento.monto
                    alcancia.monto_actual += movimiento.monto
                    safe_box.save()
                    alcancia.save()
                else:
                    raise ValidationError({"error": "Saldo insuficiente en billetera para ahorrar"})
            except Alcancia.DoesNotExist:
                raise ValidationError({"error": "No hay una alcancía activa para ahorrar"}) 