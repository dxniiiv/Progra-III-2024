from django.urls import path
from .views import CarritoView, VentaView

urlpatterns = [
path('carrito/', CarritoView.as_view()),
path('pedidos/', VentaView.as_view())
]