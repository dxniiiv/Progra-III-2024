from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistroSerializer, DireccionSerializer, CuentaSerializer, UsuarioUpdateSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Direccion, Usuario
# Create your views here.

class RegistroView(APIView):
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'El usuario ha sido registrado con exito'})
    
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        usuario = self.obtener_usuario(request.data)
        if usuario is not None:
            respuesta = super().post(request, *args, **kwargs)
            
            respuesta.data['usuario'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'roles': usuario.roles.values_list('nombre', flat=True)
            }
            print(respuesta.data['usuario'])
            return respuesta
    def obtener_usuario(self, data):
        from django.contrib.auth import get_user_model
        Usuario = get_user_model()
        correo = data.get('correo')
        try:
            return Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return None
            
    


class CuentaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        serializer = CuentaSerializer(usuario)
        return Response(serializer.data)
    
    def put(self, request):
        usuario = request.user
        serializer = UsuarioUpdateSerializer(usuario, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request):
        usuario = request.user
        usuario.delete()
        return Response({'El usuario ha sido eliminado con exito'})
    
class DireccionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        usuario = request.user
        direccion = usuario.direcciones.get(id=id)
        print(direccion)
        if not direccion:
            return Response({'mensaje': 'La dirección no existe dentro de tus direcciones'}, status=404)
        serializer = DireccionSerializer(direccion)
        return Response(serializer.data)
        
    def post(self, request):
        '''El serializer es:
        class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['id', 'nombre', 'direccion', 'lat', 'lon','indicaciones']
        '''
        usuario = request.user
        serializer = DireccionSerializer(data=request.data)
        print(request.data)
        #Validar y si hay un error imprimirlo
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        serializer.validarNombre(request.data['nombre'], usuario)
        serializer.save( usuario = usuario)
        return Response({'Direccion guardada'}, status=201)
    
    def put(self, request, id):
        usuario = request.user
        direccion = usuario.direcciones.get(id=id)
        if not direccion:
            return Response({'mensaje': 'La dirección no existe dentro de tus direcciones'}, status=404)
        serializer = DireccionSerializer(direccion, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class DireccionListaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        direcciones = usuario.direcciones.all()
        serializer = DireccionSerializer(direcciones, many=True)
        return Response(serializer.data)