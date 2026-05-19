from django.http import JsonResponse
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from main.settings import SECRET_KEY, JWT_TOKEN_EXPIRES
from datetime import datetime, timezone
from .models import User

def create_login_cookie(token : str) ->  JsonResponse:
    response = JsonResponse({'message': 'Логин успешен'})
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=JWT_TOKEN_EXPIRES
    )
    return response


def create_jwt_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + JWT_TOKEN_EXPIRES
    }

    return encode(payload, SECRET_KEY, algorithm="HS256")


def get_user_from_token(token: str) -> User:
    try:
        payload = decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        if user_id:
            return User.objects.get(id=user_id, is_active=True)
    except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
        pass
    return None