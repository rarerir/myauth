from rest_framework import authentication
from api.auth_utils import get_user_from_token

class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
            user = get_user_from_token(token)
        else:
            token = request.COOKIES.get('access_token')
            if token:
                user = get_user_from_token(token)
        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'