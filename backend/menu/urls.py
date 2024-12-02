from django.urls import path
from .views import CategoriaView, ListaProductosView, DetalleProductoView

urlpatterns = [
    path('categorias/', CategoriaView.as_view()),
    path('productos/', ListaProductosView.as_view()),
    path('producto/<int:id>/', DetalleProductoView.as_view()),
]