from .models import User
from .auth_utils import get_user_from_token

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = User.guest()
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
            user = get_user_from_token(token)
            if user is not None:
                request.user = user
        else:
            token = request.COOKIES.get('access_token')
            if token:
                user = get_user_from_token(token)
                if user is not None:
                    request.user = user
        return self.get_response(request)
