from django.http import JsonResponse
from rest_framework.decorators import action

from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils
from apps.knowledge_mgmt.manual_knowledge_mgmt.serializers import ManualKnowledgeSerializer
from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class ManualKnowledgeViewSet(AuthViewSet):
    queryset = ManualKnowledge.objects.all()
    serializer_class = ManualKnowledgeSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @action(methods=["POST"], detail=False)
    def create_manual_knowledge(self, request):
        kwargs = request.data
        new_doc = KnowledgeDocumentUtils.get_new_document(kwargs, request.user.username)
        knowledge_obj = ManualKnowledge.objects.create(
            knowledge_document_id=new_doc.id,
            content=kwargs.get("content", ""),
        )
        return JsonResponse({"result": True, "data": knowledge_obj.id})
