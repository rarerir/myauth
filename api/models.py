from django.db import models
from jwt import encode

class Role(models.Model):
    ROLES = {
        "G": "Guest",
        "U": "User",
        "A": "Admin",
    }
    shirt_size = models.CharField(max_length=1, choices=ROLES)


class User(models.Model):
    email = models.EmailField('Почта')
    password = models.CharField('Пароль', max_length=128)
    name = models.CharField('Имя', max_length=60, null=True, blank=True)
    surname = models.CharField('Фамилия', max_length=60, null=True, blank=True)
    patronymic = models.CharField('Отчество', max_length=60, null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    role = models.CharField('Роль', max_length=1, null=False)

    def encode(self):
        pass

    def __str__(self):
        return self.email


# Перевести пользовательский пароль для хранения в БД поможет библиотека
# bcrypt.
# Для создания токена из id пользователя поможет библиотека jwt.
# Можно определять пользователя из header Authorization : Bearer {user_token},
# либо после логина создавать сессию (доп таблица sessions, и в response
# устанавливать пользователю Cookie с sessionid, expire_at …
# В request сразу присваивать request.user перед обработкой запроса в
# кастомном Middleware в Django.