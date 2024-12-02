from rest_framework import serializers
from .models import Anuncio, Pregunta_Frecuente

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['id', 'imagen', 'url_redireccion']
        
class PreguntaFrecuenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta_Frecuente
        fields = ['id', 'pregunta', 'respuesta']