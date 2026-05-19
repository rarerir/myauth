from rest_framework import serializers

from api.models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password_hash', 'name', 'surname', 'patronymic', 'is_active', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }