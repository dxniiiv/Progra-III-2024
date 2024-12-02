from django.urls import path
from .views import RegistroView, LoginView, CuentaView, DireccionView, DireccionListaView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('registro/', RegistroView.as_view()),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('direcciones/', DireccionListaView.as_view()),
    path('direcciones/<int:id>/', DireccionView.as_view()),
    path('direccion/', DireccionView.as_view()),
    path('cuenta/', CuentaView.as_view()),
]