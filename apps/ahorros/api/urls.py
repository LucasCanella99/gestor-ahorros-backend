from rest_framework.routers import DefaultRouter
from apps.ahorros.api.views.movimiento_view import MovimientoViewSet
from apps.ahorros.api.views.safebox_view import SafeBoxViewSet
from apps.ahorros.api.views.alcancia_view import AlcanciaViewSet
from apps.ahorros.api.views.register_view import RegisterViewSet

router = DefaultRouter()

router.register(r'movimientos', MovimientoViewSet,basename= 'movimiento')
router.register(r'safeboxes', SafeBoxViewSet,basename= 'safebox')
router.register(r'alcancias', AlcanciaViewSet,basename= 'alcancia')
router.register(r'register',RegisterViewSet,basename='register')

urlpatterns = router.urls


