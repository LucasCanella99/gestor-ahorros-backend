from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from apps.ahorros.api.serializers.register_serializer import ResgisterSerializer

class RegisterViewSet(CreateModelMixin,GenericViewSet): 
    queryset = User.objects.all()
    serializer_class = ResgisterSerializer
    permission_classes = [AllowAny]
    
