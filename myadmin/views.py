from rest_framework import viewsets

from api.models import Role, User
from myadmin.serializers import RoleSerializer, UserSerializer
from myauth.permissions import RoleBasedPermission

class RolesApi(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ['get']
    permission_classes = [RoleBasedPermission]


class UsersApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RoleBasedPermission]