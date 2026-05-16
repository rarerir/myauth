from django.urls import path
from auth1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('auth/', views.auth, name='auth'),
    path('profile/logout', views.profile, name='logout')
]
