# TODO: тестовое задание myauth

## Уже сделано

- [x] Модель `User` (email, пароль, ФИО, `is_active`, `role`)
- [x] API ViewSet: `/api/users/`, `/api/roles/`
- [x] Тестовые пользователи (`python manage.py seed_users`)
- [x] Заглушки HTML (login, register, profile)

---

## День 1 — Аутентификация

### Модели и пароли

- [ ] Убрать пароль из `UserSerializer` в ответе API (`write_only` или не отдавать)
- [ ] `set_password()` / `check_password()` через **bcrypt** (не хранить plaintext)
- [ ] Модель **UserSession** (`user`, `token_id`, `expires_at`)
- [ ] Привести **Role** в порядок (сейчас `shirt_size` — заменить на нормальное поле, например `code` / `name`)
- [ ] Связать `User.role` с `Role` (FK или согласованные коды G/U/A)
- [ ] Миграции + проверка в shell

### Login / logout / register

- [ ] `POST /api/auth/register/` — email, пароль×2, ФИО
- [ ] `POST /api/auth/login/` — email + пароль → JWT + cookie `sessionid`
- [ ] `POST /api/auth/logout/` — удалить сессию в БД
- [ ] **Middleware**: `Authorization: Bearer` / cookie → `request.user`
- [ ] **DRF** `CustomTokenAuthentication` (чтобы DRF не затирал user)

### Профиль

- [ ] `GET /api/auth/profile/`
- [ ] `PATCH /api/auth/profile/` — редактирование ФИО
- [ ] `DELETE /api/auth/profile/` — `is_active=False`, удалить сессии, logout

**Проверка:** register → login → запрос с token → logout → снова **401**.

---

## День 2 — Авторизация и сдача

### RBAC (таблицы)

- [ ] Модель **BusinessElement** (`users`, `products`, `stores`, `orders`, `access_rules`)
- [ ] Модель **AccessRoleRule** (7 bool-полей из ТЗ)
- [ ] Команда **seed** ролей, ресурсов, правил, пользователей
- [ ] Описать схему в **README.md**

### Проверка прав

- [ ] Файл `permissions.py`: `has_permission(user, resource, action, owner_id?)`
- [ ] Логика: `read_all` vs `read` только свои (`owner_id`)
- [ ] Везде **401** (не залогинен) и **403** (нет права)

### Mock-бизнес

- [ ] Списки в коде с полем `owner_id`
- [ ] `GET /api/products/`, `stores/`, `orders/`, `users/`
- [ ] `POST /api/orders/` (create), `PATCH/DELETE /api/<resource>/<id>/`

### Admin API

- [ ] `GET/POST /api/admin/access-rules/` — только роль Admin
- [ ] `PATCH/DELETE /api/admin/access-rules/<id>/`

### Документация и финал

- [ ] `requirements.txt` (Django, DRF, bcrypt, PyJWT, psycopg2)
- [ ] README: установка, migrate, seed, примеры curl
- [ ] Прогон финального чеклиста из ТЗ
- [ ] *(Опционально)* Подключить HTML к API / обновить `context_processors` (`is_logged_in`)

---

## Мелочи / техдолг

- [ ] Уникальный `email` в модели
- [ ] Реализовать или убрать пустой `User.encode()` (JWT — в `auth_utils`, не в модели)
- [ ] Не светить `password` в `GET /api/users/`
- [ ] Вернуть маршруты фронта в `urls.py`, если сейчас только router

---

## Быстрые команды

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py seed_users
python manage.py runserver
```
