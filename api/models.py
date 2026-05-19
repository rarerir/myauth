from __future__ import annotations
from django.db import models

import bcrypt

class Role(models.Model):
    role = models.CharField('Роль', max_length=1)
    get = models.BooleanField('Просмотр', default=False)
    postself = models.BooleanField('Изменение собственных записей', default=False)
    postusers = models.BooleanField('Изменение всех записей', default=False)
    postroles = models.BooleanField('Изменение ролей', default=False)
    delete = models.BooleanField('Удаление из БД', default=False)

class User(models.Model):
    email = models.EmailField('Почта', unique=True)
    password_hash = models.CharField('Пароль', max_length=60, null=True)
    name = models.CharField('Имя', max_length=60, null=True, blank=True)
    surname = models.CharField('Фамилия', max_length=60, null=True, blank=True)
    patronymic = models.CharField('Отчество', max_length=60, null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    role = models.ForeignKey(Role, null=False, default=2, on_delete=models.SET_DEFAULT)

    def encode(self):
        pass

    def __str__(self):
        return self.email

    def set_password(self, password : str) -> None:
        self.password_hash = self.hash_password(password)

    def check_password(self, password : str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @staticmethod
    def guest() -> User:
        return User('guest@example.com', '4', '4', '', 'null', True, 1)

    @staticmethod
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')
# Можно определять пользователя из header Authorization : Bearer {user_token},
# либо после логина создавать сессию (доп таблица sessions, и в response
# устанавливать пользователю Cookie с sessionid, expire_at …
# В request сразу присваивать request.user перед обработкой запроса в
# кастомном Middleware в Django.
# VALUES ('a', true, true, true, true, true);
# VALUES ('m', true, true, true, false, false);
# VALUES ('u', false, true, false, false, false);
# VALUES ('g', false, false, false, false, false);