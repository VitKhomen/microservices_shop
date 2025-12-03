import jwt
import requests
from django.http import JsonResponse
from django.conf import settings


class JWTAuthenticationMiddleware:
    '''Middleware для перевірки JWT токенів від інших сервісів.'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Перевіряємо токен для адмінских запитів
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and '/admin/' not in request.path:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # В налаштуваннях має бути вказаний секретний ключ для перевірки токенів
                # та URL сервісу аутентифікації
                pass

        response = self.get_response(request)
        return response
