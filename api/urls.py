from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import RolesApi, UsersApi

router = routers.DefaultRouter()
router.register('admin/roles', RolesApi, basename='role')
router.register('admin/users', UsersApi, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', views.admin),
    path('register/', views.register),
    path('login/', views.login),
    path('profile/', views.profile),
    path('profile/logout/', views.logout)

]