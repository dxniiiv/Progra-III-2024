from django.db import models

class Pregunta_Frecuente(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()
    
    class Meta:
        db_table = 'preguntas_frecuentes'
        verbose_name = 'Pregunta_Frecuente'
        verbose_name_plural = 'Preguntas_Frecuentes'
    
class Anuncio(models.Model):
    imagen = models.URLField(max_length=256)
    url_redireccion = models.ImageField(upload_to='anuncios/')
    
    class Meta:
        db_table = 'anuncios'
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'
