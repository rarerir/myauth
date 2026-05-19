from django.http import JsonResponse
from rest_framework.views import APIView

from .data import *
from main.permissions import RoleBasedPermission

class MockViewProduct(APIView):
    basename = 'product'
    permission_classes = [RoleBasedPermission]

    def get(self, request):
        return JsonResponse(products, safe=False)

    def post(self, request):
        return JsonResponse(data={"message": "Продукт добавлен"}, status=200)

    def delete(self, request):
        return JsonResponse(data={"message": "Продукт удалён"}, status=200)


class MockViewOrder(APIView):
    basename = 'order'
    permission_classes = [RoleBasedPermission]

    def get(self, request):
        return JsonResponse(orders, safe=False)

    def post(self, request):
        return JsonResponse(data={"message": "Заказ добавлен"}, status=200)

    def delete(self, request):
        return JsonResponse(data={"message": "Заказ удалён"}, status=200)
