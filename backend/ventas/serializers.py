from rest_framework import serializers
from .models import Carrito, Carrito_Producto, Venta, Venta_Producto
from menu.models import Producto


class CarritoSerializer(serializers.ModelSerializer):
    id_direccion = serializers.IntegerField(source='direccion.id', required=False)
    productos = serializers.SerializerMethodField()
    class Meta:
        model = Carrito
        fields = ['productos', 'tipo_entrega', 'metodo_pago', 'id_direccion']
    def get_productos(self, obj):
        carrito_productos = obj.productos.all()
        if not carrito_productos:
            return []
        productos = []
        for carrito_producto in carrito_productos:
            id = carrito_producto.id
            nombre = carrito_producto.producto.nombre
            imagen = carrito_producto.producto.url_foto
            cantidad = carrito_producto.cantidad
            seleccionado = carrito_producto.seleccionado
            precio = carrito_producto.producto.precio
            carrto_producto_ingredientes = carrito_producto.ingredientes.all()
            
            for carrito_producto_ingrediente in carrto_producto_ingredientes:
                ingrediente = carrito_producto_ingrediente.Ingrediente
                cantidad_ingrediente = carrito_producto_ingrediente.cantidad
                precio += ingrediente.precio * cantidad_ingrediente
            
            productos.append({
                'id': id,
                'nombre': nombre,
                'imagen': imagen,
                'precio': precio,
                'cantidad': cantidad,
                'seleccionado': seleccionado
            })
        return productos