from django.urls import path
from .views import ChatView

urlpatterns = [
    #version_ia=${versionIA}&idCliente=${idCliente}
    path('mensajes', ChatView.as_view()),
]