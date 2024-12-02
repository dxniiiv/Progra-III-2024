from django.shortcuts import render
from rest_framework.response import Response
from .models import Anuncio
from rest_framework.views import APIView
from .serializers import AnuncioSerializer
from rest_framework import status

# Create your views here.
class AnuncioView(APIView):
    def get(self, request):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)
    def post(self, request):
        usuario = request.user
        if usuario.roles.filter(nombre='Administrador').exists():
            serializer = AnuncioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
            
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'mensaje': 'No tienes permisos para realizar esta acción'})
