from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import RolesApi, UsersApi

router = routers.DefaultRouter()
router.register('roles', RolesApi, basename='role')
router.register('users', UsersApi, basename='user')

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('profile/', views.profile),
    path('profile/logout', views.logout)
]

urlpatterns = [
    path('', include(router.urls))
]
