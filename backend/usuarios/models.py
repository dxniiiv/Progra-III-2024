from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, correo, nombre, apellido, telefono, password = None):
        if not correo.strip():
            raise ValueError('El correo es obligatorio')
        if not nombre.strip():
            raise ValueError('El nombre es obligatorio')
        if not apellido.strip():
            raise ValueError('El apellido es obligatorio')
        
        usuario = self.model(correo=self.normalize_email(correo),
                            nombre=nombre, apellido=apellido, 
                            telefono=telefono)
        if password:
            usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
        
class Usuario(AbstractBaseUser):
    username = None
    correo = models.EmailField(max_length=200, unique=True, error_messages={'unique': 'Ya existe una cuenta registrada con este correo'})
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'correo'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    def __str__(self):
        return self.correo
    
    def get_by_natural_key(self, correo):
        return self.get(correo=correo)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    usuarios = models.ManyToManyField(Usuario, related_name='roles')
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
class Direccion(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.TextField()
    lat = models.DecimalField(max_digits=18, decimal_places=15)
    lon = models.DecimalField(max_digits=18, decimal_places=15)
    indicaciones = models.TextField(null=True, blank=True)
    predeterminada = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    
    class Meta:
        db_table = 'direcciones'
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
