from usuarios.models import Usuario, Direccion, Rol
from rest_framework import viewsets, permissions
from .serializers import RegistroSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    
    http_method_names=['post']
    def create(self, request):
        serializer = RegistroSerializer(data=request.data)
