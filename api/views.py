from rest_framework import viewsets, generics, permissions

from .models import Role, User
from .serializers import RoleSerializer, UserSerializer


class RolesApi(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ['get']


class UsersApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
