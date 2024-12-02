from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ChatSerializer, ListaClientesSerializer
from rest_framework.response import Response
from .models import Mensaje
from usuarios.models import Usuario
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        id_cliente = request.query_params.get('id_cliente')
        version_ia = request.query_params.get('version_ia', 'false').lower() == 'true'
        print('id_cliente: ', id_cliente)
        print('version_ia: ', version_ia)
        tipo_usuario = 'cliente' if usuario.roles.filter(nombre='Cliente').exists() else 'empleado' if usuario.roles.filter(nombre='Atención al cliente').exists() else None
        if not tipo_usuario:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
        cliente = Usuario.objects.get(id=id_cliente)
        if not cliente:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'mensaje': 'No se encontró el cliente'})
        serializer = ChatSerializer(cliente, context={'id_cliente': id_cliente, 'version_ia': version_ia, 'tipo_usuario': tipo_usuario})
        return Response(serializer.data)
    
    def post(self,request):
        usuario = request.user
        id_cliente = request.data.get('id_cliente')
        contenido = request.data.get('contenido')
        tipo_usuario = 'cliente' if usuario.roles.filter(nombre='Cliente').exists() else 'empleado' if usuario.roles.filter(nombre='Atención al cliente').exists() else None
        if not tipo_usuario:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
        cliente = Usuario.objects.get(id=id_cliente)
        if not cliente:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'mensaje': 'No se encontró el cliente'})
        
        por = 'cliente' if tipo_usuario == 'cliente' else 'empleado'
        modo = 'empleado'
        mensaje = Mensaje.objects.create(cliente=cliente, por=por, modo=modo, contenido=contenido)
        mensaje.save()
        return Response(status=status.HTTP_201_CREATED, data={'mensaje': 'Mensaje enviado'})
    
class ListaClientes(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        if not usuario.roles.filter(nombre='Atención al cliente').exists():
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
        serializer = ListaClientesSerializer(Usuario, many=True)
        return Response(serializer.data)