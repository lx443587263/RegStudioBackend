import jwt
from django.conf import settings


def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')
