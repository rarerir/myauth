from django.urls import path, include
from rest_framework import routers

from .views import RolesApi, UsersApi

router = routers.DefaultRouter()
router.register('roles', RolesApi, basename='role')
router.register('users', UsersApi, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]