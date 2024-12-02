"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import jwt
from django.conf import settings
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
django_app = get_asgi_application()

application = socketio.ASGIApp(sio, django_app)

connected_users = {}

@sio.event
async def connect(sid, environ):
    token = environ.get('HTTP_AUTHORIZATION','').split("bearer ")[-1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        id_usuario = payload['user_id']
        connected_users[id_usuario] = sid
        print("Usuario conectado :", id_usuario)
        
    except jwt.ExpiredSignatureError:
        print("Token expirado")
        sio.disconnect(sid)
    except jwt.InvalidTokenError:
        print("Token invalido")
        sio.disconnect(sid)

@sio.event
async def disconnect(sid):
    for id_usuario, socket_id in connected_users.items():
        if socket_id == sid:
            del connected_users[id_usuario]
            print("Usuario desconectado :", id_usuario)
            break
    

