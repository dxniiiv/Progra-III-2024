from django.db import models
from usuarios.models import Usuario
import enum

class Mensaje(models.Model):
    POR_CHOICES = [
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
    ]
    MODO_CHOICES = [
        ('empleado', 'Empleado'),
        ('bot', 'Bot'),
    ]
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes')
    por = models.CharField(max_length=10, choices=POR_CHOICES, default='cliente')
    modo = models.CharField(max_length=10, choices=MODO_CHOICES, default='empleado')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mensajes'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'