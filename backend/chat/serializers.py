from rest_framework import serializers
from .models import Mensaje
from usuarios.models import Usuario

class ChatSerializer(serializers.ModelSerializer):
    mensajes = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ['mensajes']
    
    def get_mensajes(self, obj):
        id_cliente = self.context.get('id_cliente')
        version_ia = self.context.get('version_ia')
        tipo_usuario = self.context.get('tipo_usuario')
        
        if not id_cliente:
            return []
        
        cliente = Usuario.objects.get(id=id_cliente)
        
        if version_ia:
            mensajes = Mensaje.objects.filter(cliente=cliente, modo='bot')
        else:
            mensajes = Mensaje.objects.filter(cliente=cliente, modo='empleado')
        
        return [
            {   
                'id': m.id,
                'fecha': m.fecha,
                'contenido': m.contenido,
                'enviado': True if m.por == 'cliente' and tipo_usuario == 'cliente' else False,
            }
            for m in mensajes
        ]

class ListaClientesSerializer(serializers.ModelSerializer):
    ultimo_mensaje = serializers.SerializerMethodField()
    fecha_ultimo_mensaje = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'ultimo_mensaje', 'fecha_ultimo_mensaje']
    
    def get_ultimo_mensaje(self, obj):
        mensajes = Mensaje.objects.filter(cliente=obj, modo='empleado').order_by('-fecha')
        if not mensajes.exists():
            return "NUEVO CLIENTE"
        return mensajes.first().contenido

    def get_fecha_ultimo_mensaje(self, obj):
        mensajes = Mensaje.objects.filter(cliente=obj, modo='empleado').order_by('-fecha')
        if not mensajes.exists():
            return obj.fecha_registro
        return mensajes.first().fecha
