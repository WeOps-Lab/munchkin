from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action

from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.knowledge_mgmt.knowledge_base_mgmt.serializers import KnowledgeBaseSerializer
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class KnowledgeBaseViewSet(AuthViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @HasRole()
    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", "")
        queryset = KnowledgeBase.objects.filter(name__icontains=name)
        if not request.user.is_superuser:
            teams = [i["id"] for i in request.user.group_list]
            queryset = queryset.filter(team__in=teams)
        return self._list(queryset)

    @HasRole()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @HasRole()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        if KnowledgeDocument.objects.filter(knowledge_base_id=kwargs["pk"]).exists():
            return JsonResponse(
                {"result": False, "message": _("This knowledge base contains documents and cannot be deleted.")}
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    @HasRole()
    def get_teams(self, request):
        if not hasattr(request, "user"):
            token = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[-1]
            client = KeyCloakClient()
            _, user_info = client.token_is_valid(token)
            groups = client.get_user_groups(user_info["sub"], "admin" in user_info["realm_access"]["roles"])
        else:
            groups = request.user.group_list
        return JsonResponse({"result": True, "data": groups})
