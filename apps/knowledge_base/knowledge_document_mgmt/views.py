from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action

from apps.core.decorators.api_perminssion import HasRole
from apps.knowledge_base.knowledge_document_mgmt.serializers import KnowledgeDocumentSerializer
from apps.knowledge_base.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_base.viewset_utils import AuthViewSet


class KnowledgeDocumentViewSet(AuthViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @HasRole()
    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", "")
        knowledge_base_id = request.GET.get("knowledge_base_id", 0)
        if not knowledge_base_id:
            return JsonResponse({"result": False, "message": _("{} is required").format("knowledge_base_id")})
        queryset = KnowledgeDocument.objects.filter(knowledge_base_id=knowledge_base_id, name__icontains=name)
        if not request.userinfo.get("is_superuser"):
            teams = [i["id"] for i in request.userinfo.get("teams", [])]
            queryset = queryset.filter(knowledge_base__team__in=teams)
        return self._list(queryset)

    @staticmethod
    def has_auth(user_info, knowledge_base_id):
        is_super = user_info.get("is_superuser")
        teams = [i["id"] for i in user_info.get("teams", [])]
        return is_super or KnowledgeBase.objects.filter(id=knowledge_base_id, team__in=teams).exists()

    @HasRole()
    @action(methods=["POST"], detail=False)
    def create_local_fie_doc(self, request):
        kwargs = request.data
        self.validate_create_kwargs(request.userinfo, kwargs)
        file_data = request.FILES.getlist("file", [])
        if not file_data:
            return JsonResponse({"result": False, "message": _("{} is required").format("file")})

    @classmethod
    def validate_create_kwargs(cls, userinfo, kwargs):
        if not kwargs.get("knowledge_base_id"):
            raise Exception(_("{} is required").format("knowledge_base_id"))
        is_super = userinfo.get("is_superuser")
        teams = [i["id"] for i in userinfo.get("teams", [])]
        has_auth = is_super or KnowledgeBase.objects.filter(id=kwargs["knowledge_base_id"], team__in=teams).exists()
        if not has_auth:
            raise Exception(_("insufficient permissions"))

    @HasRole()
    def create_web_link(self, request):
        kwargs = request.data
        self.validate_create_kwargs(request.userinfo, kwargs)
        if not kwargs.get("web_link"):
            return JsonResponse({"result": False, "message": _("{} is required").format("web_link")})

    @HasRole()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
