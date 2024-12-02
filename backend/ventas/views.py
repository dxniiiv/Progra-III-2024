from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# importar modelo producto
from menu.models import Producto, Producto_Tipo_Ingrediente, Ingrediente, Tipo_Ingrediente
from usuarios.models import Usuario, Direccion
from .models import Carrito, Carrito_Producto, Venta, Venta_Producto, Ingrediente, Carrito_Producto_Ingrediente
from rest_framework import status
from .serializers import CarritoSerializer

class CarritoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        carrito = usuario.carrito
        serializer = CarritoSerializer(carrito)
        return Response(serializer.data)
    
    def post(self, request):
        usuario = request.user
        carrito = usuario.carrito
        detalles = request.data.get('detalles')
        cantidad = request.data.get('cantidad')
        ingredientes_obtenidos = request.data.get('ingredientes')
        id = request.data.get('id')
        producto = Producto.objects.filter(id=id).first()

        if not producto:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'mensaje': 'Producto no encontrado'})
        carrito_producto = Carrito_Producto.objects.create(
            carrito=carrito,
            producto=producto,
            cantidad=cantidad,
            detalles=detalles,
            seleccionado=True
        )
        carrito_producto.save()
        
        if ingredientes_obtenidos:
            for i in ingredientes_obtenidos:
                if i['cantidad'] > 0:
                    ingrediente = Ingrediente.objects.filter(id=i['id']).first()
                    carrito_producto_ingrediente = Carrito_Producto_Ingrediente.objects.create(
                        carrito_producto=carrito_producto,
                        Ingrediente=ingrediente,
                        cantidad=i['cantidad']
                    )
                    carrito_producto_ingrediente.save()
        return Response(status=status.HTTP_201_CREATED, data={'mensaje': 'Producto añadido al carrito correctamente'})
    def put(self, request):
        usuario = request.user
        productos = request.data.get('productos')
        tipo_entrega = request.data.get('tipo_entrega')
        metodo_pago = request.data.get('metodo_pago')
        print('metodo_pago: ', metodo_pago)
        id_direccion = request.data.get('id_direccion')
        
        carrito = usuario.carrito
        for producto in productos:
            print(producto)
            #Obtener el carrito_producto correspondiente si existe y modificarlo, si no, devolver error
            carrito_producto = Carrito_Producto.objects.get(id=producto['id'])
            if carrito_producto:
                
                carrito_producto.cantidad = producto['cantidad'] if producto['cantidad'] > 0 else 1
                carrito_producto.seleccionado = producto['seleccionado']
                carrito_producto.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'El producto no está en el carrito'})
        carrito.tipo_entrega = tipo_entrega
        carrito.metodo_pago = metodo_pago
        if id_direccion:
            carrito.direccion = Direccion.objects.get(id=id_direccion)
        carrito.save()
        return Response(status=status.HTTP_200_OK, data={'mensaje': 'Carrito actualizado correctamente'})
    
    def delete(self, request):
        usuario = request.user
        carrito = Carrito.objects.filter(usuario=usuario)
        ids = request.data.get('ids')
        productos_a_eliminar = []
        for id in ids:
            carrito_producto = Carrito_Producto.objects.get(id=id)
            if carrito_producto:
                productos_a_eliminar.append(carrito_producto)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': f'No se encontró el producto con id {id}'})
        for producto in productos_a_eliminar:
            producto.delete()
        return Response(status=status.HTTP_200_OK, data={'mensaje': 'Productos eliminados correctamente'})

class VentaView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        usuario = request.user
        carrito = usuario.carrito
        productos = request.data.get('productos')
        tipo_entrega = request.data.get('tipo_entrega')
        print(request.data.get('id_direccion'))
        id_direccion = request.data.get('id_direccion')
        metodo_pago = request.data.get('metodo_pago')
        print('id_direccion: ', id_direccion)
        print('tipo_entrega: ', tipo_entrega)
        print('metodo_pago: ', metodo_pago)
        print('productos: ', productos)
        if not productos:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'No se enviaron productos'})
        direccion = Direccion.objects.get(id=id_direccion)
        venta = Venta.objects.create(
            usuario=usuario,
            tipo_entrega=tipo_entrega,
            metodo_pago=metodo_pago,
            direccion=direccion
        )
        venta.save()
        
        for producto in productos:
            print(producto['id'])
            producto_guardado = Producto.objects.get(id = producto['id'])
            print("Producto guardado:")
            print(producto_guardado)
            venta_producto = Venta_Producto()
            venta_producto.venta = venta
            venta_producto.producto = producto_guardado
            venta_producto.cantidad = producto['cantidad']
            venta_producto.precio_compra = producto_guardado.precio
            venta_producto.save()
        return Response(status=status.HTTP_201_CREATED, data={'mensaje': 'Venta realizada correctamente'})
            
        