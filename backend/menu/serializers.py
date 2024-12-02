from rest_framework import serializers
from .models import Categoria, Producto, Ingrediente, Tipo_Ingrediente, Producto_Tipo_Ingrediente, Descuento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre','url_foto']
        
class ProductoListaSerializer(serializers.ModelSerializer):
    #Estos valores pueden ser nulos
    valor_descuento = serializers.CharField(source='descuento.valor', allow_null=True)
    tipo_descuento = serializers.CharField(source='descuento.tipo', allow_null=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion','precio', 'valor_descuento', 'tipo_descuento', 'url_foto']

"""
Ejemplo de JSON que se espera en la vista de Ingredientes elegibles para un producto
seleccion_ingredientes : [
    {
        titulo: 'Selecciona el tipo de carne',
        minimo: 1,
        maximo: 1,
        multiple: false,
        ingredientes: [
            {
                id: 1,
                nombre: 'Carne de res'
            },
            {
                id: 2,
                nombre: 'Carne de pollo'
            }
        ]
    },
    {
        titulo: 'Elige ingredientes adicionales (máximo 4)',
        minimo: 0,
        maximo: 4,
        multiple: true,
        ingredientes: [
            {
                id: 3,
                nombre: 'Queso',
                precio: 1.15
            },
            {
                id: 4,
                nombre: 'Tocino',
                precio: 0.75
            }
        ]
    }
    
]

"""

class ProductoDetalleSerializer(serializers.ModelSerializer):
    precio = serializers.SerializerMethodField()
    precio_anterior = serializers.SerializerMethodField()
    categoria = serializers.SerializerMethodField()
    imagen = serializers.CharField(source='url_foto')
    seleccion_ingredientes = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = ['id', 'nombre','descripcion', 'categoria', 'precio', 'precio_anterior','imagen', 'seleccion_ingredientes']

    def get_precio(self, obj):
        if obj.descuento:
            if obj.descuento.tipo == 'porcentaje':
                return obj.precio - (obj.precio * obj.descuento.valor / 100)
            return obj.precio - obj.descuento.valor
        return obj.precio
    
    def get_precio_anterior(self, obj):
        if obj.descuento:
            return obj.precio
        return None
    
    def get_categoria(self, obj):
        return obj.categoria.nombre
    
    def get_seleccion_ingredientes(self, obj):
        seleccion_ingredientes = []
        relacion = Producto_Tipo_Ingrediente.objects.filter(producto=obj)
        
        for r in relacion:
            id_tipo = r.id
            tipo_ingrediente = r.tipo_ingrediente
            ingredientes = tipo_ingrediente.ingredientes.all()
            minimo = r.minimo
            maximo = r.maximo
            multiple = r.multiple
            titulo = r.mensaje
            
            # Añadir los datos a seleccion_ingredientes

            seleccion_ingredientes.append({
                'id_tipo': id_tipo,
                'titulo': titulo,
                'minimo': minimo,
                'maximo': maximo,
                'multiple': multiple,
                'ingredientes': [
                    {
                        'id': i.id,
                        'nombre': i.nombre,
                        'precio': i.precio
                    } for i in ingredientes
                ]
            })
        return seleccion_ingredientes