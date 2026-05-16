from django.urls import path
from mainprogram import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('profile/logout/', views.logout, name='logout')
]
