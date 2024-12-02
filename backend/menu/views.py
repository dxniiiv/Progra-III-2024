from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CategoriaSerializer, ProductoListaSerializer, ProductoDetalleSerializer
from rest_framework.response import Response
from .models import Categoria, Producto, Descuento
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CategoriaView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            # Permitir acceso público a las solicitudes GET
            return [AllowAny()]
        else:
            # Requerir autenticación para POST, PUT, DELETE
            return [IsAuthenticated()]
        
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        usuario = request.user
        if usuario.roles.filter(nombre='Administrador').exists():
            serializer = CategoriaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
            
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
    def put(self, request):
        usuario = request.user
        if usuario.roles.filter(nombre='Administrador').exists():
            categoria = Categoria.objects.get(id=request.data['id'])
            serializer = CategoriaSerializer(categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
            
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
    
    def delete(self, request):
        usuario = request.user
        if usuario.roles.filter(nombre='Administrador').exists():
            categoria = Categoria.objects.get(id=request.data['id'])
            categoria.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
class ListaProductosView(APIView):
    def get(self, request):
        categoria = request.query_params.get('categoria')
        filtro = request.query_params.get('filtro')
        
        productos = Producto.objects.all()
        if categoria:
            productos = productos.filter(categoria__nombre=categoria)
        if filtro:
            productos = productos.filter(nombre__icontains=filtro)
        serializer = ProductoListaSerializer(productos, many=True)
        return Response(serializer.data)
class DetalleProductoView(APIView):
    def get(self, request, id):
        producto = Producto.objects.get(id=id)
        serializer = ProductoDetalleSerializer(producto)
        return Response(serializer.data)

