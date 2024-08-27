from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.base.models import UserAPISecret
from apps.base.user_api_secret_mgmt.serializers import UserAPISecretSerializer
from apps.core.decorators.api_perminssion import HasRole


class UserAPISecretViewSet(viewsets.ModelViewSet):
    queryset = UserAPISecret.objects.all()
    serializer_class = UserAPISecretSerializer
    ordering = ("-id",)
    search_fields = ("username",)

    @action(detail=False, methods=["POST"])
    def generate_api_secret(self, request):
        api_secret = UserAPISecret.generate_api_secret()
        return JsonResponse({"result": True, "data": {"api_secret": api_secret}})

    @HasRole("admin")
    def create(self, request, *args, **kwargs):
        if UserAPISecret.objects.filter(username=request.data["username"]).exists():
            return JsonResponse({"result": False, "message": "该用户已存在API密钥"})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return JsonResponse({"result": False, "message": "API密钥不支持修改"})

    @HasRole("admin")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
