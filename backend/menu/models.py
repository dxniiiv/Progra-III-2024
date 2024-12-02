from django.db import models
import enum
import datetime
# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    url_foto = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        
class Descuento(models.Model):
    TIPO_CHOICES = [
        ('porcentaje', 'Porcentaje'),
        ('fijo', 'Fijo'),
    ]
    FREQ_CHOICES = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    ]
    
    nombre = models.CharField(max_length=50, default='Descuento')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='porcentaje')
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    inicio = models.DateTimeField(default=datetime.datetime.now())
    fin = models.DateTimeField(default=datetime.datetime.now())
    frecuencia = models.CharField(max_length=10, choices=FREQ_CHOICES, null=True, blank=True)
    
    class Meta:
        db_table = 'descuentos'
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    url_foto = models.CharField(max_length=256)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, related_name='productos', null=True, blank=True)
    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        
class Combo_Producto(models.Model):
    combo = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='combos')
    cantidad = models.IntegerField()
    
    class Meta:
        db_table = 'combos_productos'
        verbose_name = 'Combo_Producto'
        verbose_name_plural = 'Combos_Productos'

class Tipo_Ingrediente(models.Model):
    nombre = models.CharField(max_length=50)
    class Meta:
        db_table = 'tipo_ingredientes'
        verbose_name = 'Tipo_Ingrediente'
        verbose_name_plural = 'Tipos_Ingrediente'
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_ingrediente = models.ForeignKey(Tipo_Ingrediente, on_delete=models.CASCADE, related_name='ingredientes')
    
    class Meta:
        db_table = 'ingredientes'
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'

class Producto_Tipo_Ingrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='tipos_ingrediente')
    tipo_ingrediente = models.ForeignKey(Tipo_Ingrediente, on_delete=models.CASCADE, related_name='productos')
    minimo = models.IntegerField()
    maximo = models.IntegerField(null=True)
    mensaje = models.CharField(max_length=255, null=True)
    multiple = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'productos_tipos_ingredientes'
        verbose_name = 'Producto_Tipo_Ingrediente'
        verbose_name_plural = 'Productos_Tipos_Ingredientes'
    