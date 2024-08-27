from django.http import JsonResponse
from rest_framework import viewsets

from apps.base.models import UserAPISecret
from apps.core.decorators.api_perminssion import HasRole
from apps.knowledge_base.knowledge_base_mgmt.serializers import KnowledgeBaseSerializer
from apps.knowledge_base.models import KnowledgeBase


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    ordering = ("-id",)
    search_fields = ("name",)

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
