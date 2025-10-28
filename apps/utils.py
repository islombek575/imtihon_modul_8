from django.conf import settings
from django.core.cache import cache
from redis import Redis
from rest_framework import status
from rest_framework.exceptions import ValidationError


def get_login_data(phone):
    return f"login:{phone}"


def send_code(phone: str, code: int, expired_time=3600):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _phone = get_login_data(phone)
    _ttl = redis.ttl(f':1:{_phone}')

    if _ttl > 0:
        return False, _ttl

    print(f'Phone: {phone} == Code: {code}')
    cache.set(_phone, code, expired_time)
    return True, 0


def check_phone(phone: str, code: int):
    _phone = get_login_data(phone)
    _code = cache.get(_phone)
    if _code is None:
        raise ValidationError('Invalid phone number', status.HTTP_404_NOT_FOUND)
    print(code, _code)
    return _code == code