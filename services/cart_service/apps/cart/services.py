import requests
import logging
from django.conf import settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ProductServices:
    '''Сервіс для взаємодії з сервісом продуктів'''

    @staticmethod
    def get_product(product_id: int) -> Optional[Dict[str, Any]]:
        '''Отримання інформації о товарі'''
        try:
            response = requests.get(
                f'{settings.PRODUCT_SERVICE_URL}/api/products/{product_id}',
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to get product {product_id}: {e}')
            return None

    @staticmethod
    def check_availability(product_id: int, quantity: int) -> bool:
        '''Перевірка наявності на складі'''
        try:
            response = requests.get(
                f'{settings.PRODUCT_SERVICE_URL}/api/products/{product_id}/check-availability/',
                params={'quantity': quantity},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('available', False)
            return False
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Failed to check availability for product {product_id}: {e}")
            return False


class UserService:
    '''Сервіс для взаімодії з User Service'''

    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        '''Інформація про користувача за токеном'''
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/users/profile/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user from token: {e}")
            return None
