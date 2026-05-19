from django.urls import path
from .views import MockViewProduct

urlpatterns = [
    path('', MockViewProduct.as_view())
]
