from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import viewsets
import json

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

def admin_roles(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод запрещён'}, status=405)
    user = request.user
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # if user.role.postroles:



    return JsonResponse({'error': 'Метод запрещён'}, status=405)


def register(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод запрещён'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')
    if password1 != password2:
        return JsonResponse({'message': 'Пароли не совпадают'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Такая почта уже существует'})
    user = User(email=email)
    user.set_password(password1)
    user.role = Role.objects.get(id=2)
    user.save()
    return JsonResponse({'message': f'Пользователь {user.email} зарегистрирован'})

def login(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод запрещён'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    email = data.get('email')
    password = data.get('password')
    user = User.objects.get(email=email)
    if user is None or not user.check_password(password) or not user.is_active:
        return JsonResponse({'message': 'Неправильный пароль или почта'})
    else:
        return create_login_cookie(create_jwt_token(user))

def profile(request):
    user = request.user
    if request.method == 'POST' and user.role.postself:
        try:
            if not user.role.postself:
                return JsonResponse({'error': 'У вас нет прав на редактирование профиля'}, status=403)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Роль пользователя не найдена'}, status=403)

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        patronimic = data.get('patronimic')

        if not any([email, password, name, surname, patronimic]):
            return JsonResponse({'error': 'Нет данных для обновления'}, status=400)

        if email and email.strip():
            email = email.strip()
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({'error': 'Пользователь с таким email уже существует'}, status=400)
            user.email = email
        if password and password.strip():
            user.set_password(password.strip())
        if name and name.strip():
            user.name = name.strip()
        if surname and surname.strip():
            user.surname = surname.strip()
        if patronimic and patronimic.strip():
            user.patronimic = patronimic.strip()

        user.save()
        return JsonResponse({'message': 'Профиль успешно обновлён'}, status=200)

    if request.method == 'DELETE' and user.role.postself:
        user.is_active = False
        user.save()
        return logout(request)
    if request.method == 'GET' and user.role.get:
        return JsonResponse(model_to_dict(user, fields=['email', 'name', 'surname', 'patronymic', 'role']))
    return JsonResponse({'error': 'Метод запрещён или недостаточно прав'}, status=405)

def logout(request):
    response = JsonResponse({'message': 'Выход успешен'})
    response.delete_cookie('access_token')
    return response