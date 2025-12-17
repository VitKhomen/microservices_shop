import time

from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings


class RateLimitMiddleware:
    '''Обмеження частоти запитів'''

    def __init__(self, resp):
        self.get_response = resp

    def __call__(self, request):
        # Пропускаєм статіку і адмінку
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return self.get_response(request)

        # Отримуємо ip клієнта
        client_ip = self.get_client_ip(request)

        # Створюємо ключ для кеша
        cache_key = f"rate_limit:{client_ip}"

        # Отримуємо кількись запросів
        current_request = cache.get(cache_key, 0)

        # Перевіряємо ліміт
        if current_request > settings.RATE_LIMIT_REQUESTS_PER_MINUTE:
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {settings.RATE_LIMIT_REQUESTS_PER_MINUTE} requests per minute allowed'
            }, status=429)

        # Збільшуємо лічильник
        cache.set(cache_key, current_request + 1, 60)  # 60  секунд

        response = self.get_response(request)

        # Додаємо заголовки с інформацією по лімітам
        response['X-RateLimit-Limit'] = str(
            settings.RATE_LIMIT_REQUESTS_PER_MINUTE)
        response['X-RateLimit-Remaining'] = str(
            max(0, settings.RATE_LIMIT_REQUESTS_PER_MINUTE - current_request - 1))

        return response

    def get_client_ip(self, request):
        '''Отримуємо IP адрес клієнта'''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
