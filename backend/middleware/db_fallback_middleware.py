from django.db import connections
from django.db.utils import OperationalError
from django.utils.deprecation import MiddlewareMixin

class DatabaseFallbackMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            # Intenta conectar con la base de datos principal (MySQL)
            connection = connections['default']
            connection.ensure_connection()
        except OperationalError:
            # Si falla, cambia a la base de datos de respaldo (SQLite)
            connections['default'] = connections['sqlite']
            