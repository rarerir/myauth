from django.db import migrations, models
import django.db.models.deletion

def seed_default_roles(apps, schema_editor):
    Role = apps.get_model('api', 'Role')
    default_roles = [
        ('g', False, False, False, False, False),
        ('u', False, True, False, False, False),
        ('m', True, True, True, False, False),
        ('a', True, True, True, True, True),
    ]
    for role, get, postself, postusers, postroles, delete in default_roles:
        Role.objects.update_or_create(
            role=role,
            defaults={
                'get': get,
                'postself': postself,
                'postusers': postusers,
                'postroles': postroles,
                'delete': delete,
            },
        )


def seed_default_users(apps, schema_editor):
    User = apps.get_model('api', 'User')
    users_data = [
        ('admin@example.com', '4', '4', '4', '$2b$12$8MU9uke0Rrld5VtIwocBRuX/cuFHTlQKsHbaHHvTmvdxnR.3aF7jS', True, 4),
        ('manager@example.com', '3', '3', '3', '$2b$12$8MU9uke0Rrld5VtIwocBRuX/cuFHTlQKsHbaHHvTmvdxnR.3aF7jS', True, 3),
        ('user@example.com', '2', '2', '2', '$2b$12$8MU9uke0Rrld5VtIwocBRuX/cuFHTlQKsHbaHHvTmvdxnR.3aF7jS', True, 2),
        ('guest@example.com', '1', '1', '1', None, True, 1),
    ] # $2b$12$8MU9uke0Rrld5VtIwocBRuX/cuFHTlQKsHbaHHvTmvdxnR.3aF7jS - 11111111
    for email, name, surname, patronymic, pwd_hash, is_active, role in users_data:
        User.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'surname': surname,
                'patronymic': patronymic,
                'password_hash': pwd_hash,
                'is_active': is_active,
                'role_id': role,
            }
        )


def unseed_default_roles(apps, schema_editor):
    Role = apps.get_model('api', 'Role')
    Role.objects.filter(role__in=['a', 'm', 'u', 'g']).delete()

def unseed_default_users(apps, schema_editor):
    User = apps.get_model('api', 'User')
    User.objects.filter(id__in=[1, 2, 3, 4]).delete()

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=1, verbose_name='Роль')),
                ('get', models.BooleanField(default=False, verbose_name='Просмотр')),
                ('postself', models.BooleanField(default=False, verbose_name='Изменение собственных записей')),
                ('postusers', models.BooleanField(default=False, verbose_name='Изменение всех записей')),
                ('postroles', models.BooleanField(default=False, verbose_name='Изменение ролей')),
                ('delete', models.BooleanField(default=False, verbose_name='Удаление из БД')),
            ],
        ),
        migrations.RunPython(seed_default_roles, unseed_default_roles),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('password_hash', models.CharField(max_length=60, null=True, verbose_name='Пароль')),
                ('name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=60, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=60, null=True, verbose_name='Отчество')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.role')),
            ],
        ),
        migrations.RunPython(seed_default_users, unseed_default_users)
    ]
