from uuid import uuid4

from django.core.cache import cache


class Token:
    @classmethod
    def generate_token(cls, pk, expired=3600):
        token = uuid4()
        cache.set(token, pk, expired)
        return token

    @classmethod
    def check_token(cls, token):
        return cache.get(token)
