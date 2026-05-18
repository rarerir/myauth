from django.http import JsonResponse
from rest_framework import viewsets, generics, permissions

from .auth_utils import create_login_cookie, create_jwt_token
from .models import Role, User
from .serializers import RoleSerializer, UserSerializer


class RolesApi(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ['get']


class UsersApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def register(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод запрещён'}, status=405)

    email = request.POST.get('email')
    password1 = request.POST.get('password')
    password2 = request.POST.get('password')
    if password1 != password2:
        return JsonResponse({'message': 'Пароли не совпадают'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Такая почта уже существует'})
    user = User(email=email)
    user.set_password(password1)
    user.save()
    return JsonResponse({'message': f'Пользователь {user.email} зарегистрирован'})


def login(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод запрещён'}, status=405)
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.get(email=email)
    if user is None or not user.check_password(password):
        return JsonResponse({'message': 'Неправильный пароль или почта'})
    else:
        return create_login_cookie(create_jwt_token(user))

def profile(request) -> JsonResponse:
    user = request.user
    if not user:
        return JsonResponse({'message': '<UNK> <UNK> <UNK>'})
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if user is None or not user.check_password(password):
            return JsonResponse({'message': 'Неправильный пароль или почта'})
        else:
            return create_login_cookie(create_jwt_token(user))
    if request.method == 'DELETE':
        user.is_active = False
        logout(request)
    if request.method == 'GET':
        return JsonResponse(user.to_dict())
    return JsonResponse({'error': 'Метод запрещён'}, status=405)


def logout(request):
    response = JsonResponse({'message': 'Выход успешен'})
    response.delete_cookie('access_token')
    return response