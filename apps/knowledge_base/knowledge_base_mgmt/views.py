from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.knowledge_base.knowledge_base_mgmt.serializers import KnowledgeBaseSerializer
from apps.knowledge_base.models import KnowledgeBase


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @HasRole()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasRole()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    @HasRole("admin")
    def get_teams(self, request):
        token = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[-1]
        client = KeyCloakClient()
        groups = client.get_user_groups(token)
        return JsonResponse({"result": True, "data": groups})
