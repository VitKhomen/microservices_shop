import jwt
from django.http import JsonResponse
from django.conf import settings

from .services import UserService

import logging

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаемо health check і admin
        if request.path in ['/health/', '/admin']:
            return self.get_response(request)

        # Пропускаємо OPTIONS заприти
        if request.method == 'OPTIONS':
            return self.get_response(request)

        # Беремо токен
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer'):
            token = auth_header.split(' ')[1]
            logger.info(f"Found auth token in request to {request.path}")

            # Получаємо користувача через user-service
            user_data = UserService.get_user_from_token(token)
            if user_data:
                request.user_id = user_data['id']
                request.user_email = user_data['email']
                logger.info(
                    f"Authenticated user {user_data['id']} for {request.path}")

                response = self.get_response(request)
                return response
            else:
                logger.warning(f"Invalid token for {request.path}")
                return JsonResponse({
                    'error': 'Invalid token',
                    'message': 'The provided authentication token is invalid'
                }, status=401)
        else:
            logger.warning(f"No auth header found for {request.path}")
            return JsonResponse({
                'error': 'Authentication required',
                'message': 'Authorization header with Bearer token is required'
            }, status=401)

        # На всяк випадок
        response = self.get_response(request)
        return response
