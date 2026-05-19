from django.forms import model_to_dict
from django.http import JsonResponse
import json

from rest_framework.views import APIView

from myauth.permissions import RoleBasedPermission
from .auth_utils import create_login_cookie, create_jwt_token
from .models import User


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

def logout(request) -> JsonResponse:
    response = JsonResponse({'message': 'Выход успешен'})
    response.delete_cookie('access_token')
    return response


class ProfileAPIView(APIView):
    basename = 'user'
    permission_classes = [RoleBasedPermission]

    def get(self, request) -> JsonResponse:
        user = request.user
        data = model_to_dict(user, fields=['email', 'name', 'surname', 'patronymic', 'role'])
        return JsonResponse(data)

    def post(self, request) -> JsonResponse:
        user = request.user
        if not user.role.postself:
            return JsonResponse({'error': 'Нет прав на редактирование профиля'}, status=403)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        patronymic = data.get('patronymic')

        if not any([email, password, name, surname, patronymic]):
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
        if patronymic and patronymic.strip():
            user.patronymic = patronymic.strip()
        user.save()
        return JsonResponse({'message': 'Профиль успешно обновлён'}, status=200)

    def delete(self, request) -> JsonResponse:
        user = request.user
        if not user.role.postself:
            return JsonResponse({'error': 'Нет прав на удаление аккаунта'}, status=403)
        user.is_active = False
        user.save()
        return JsonResponse({'message': 'Аккаунт деактивирован'}, status=200)