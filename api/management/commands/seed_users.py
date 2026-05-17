from django.core.management.base import BaseCommand

from api.models import User


class Command(BaseCommand):
    help = 'Creates test users in mainprogram_user table'

    def handle(self, *args, **options):
        test_users = [
            {
                'email': 'admin@example.com',
                'password': 'password123',
                'name': 'Админ',
                'surname': 'Системный',
                'patronymic': '',
                'role': 'A',
            },
            {
                'email': 'user@example.com',
                'password': 'password123',
                'name': 'Пётр',
                'surname': 'Пользователев',
                'patronymic': 'Петрович',
                'role': 'U',
            },
            {
                'email': 'guest@example.com',
                'password': 'password123',
                'name': 'Гость',
                'surname': 'Гостев',
                'patronymic': '',
                'role': 'G',
            },
            {
                'email': 'manager@example.com',
                'password': 'password123',
                'name': 'Иван',
                'surname': 'Менеджеров',
                'patronymic': 'Иванович',
                'role': 'U',
                'is_active': True,
            },
        ]

        created_count = 0
        for data in test_users:
            password = data.pop('password')
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults=data,
            )
            if created:
                user.password = password
                user.save()
                created_count += 1
                self.stdout.write(f'Created: {user.email} (role={user.role})')
            else:
                self.stdout.write(f'Already exists: {user.email}')

        self.stdout.write(self.style.SUCCESS(f'Done. New users: {created_count}'))
