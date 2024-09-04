from django.http import JsonResponse
from rest_framework.decorators import action

from apps.knowledge_mgmt.knowledge_document_mgmt.serializers import KnowledgeDocumentSerializer
from apps.knowledge_mgmt.models import KnowledgeDocument
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class KnowledgeDocumentViewSet(AuthViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @action(methods=["POST"], detail=False)
    def preprocess(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(**kwargs)
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def preview(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        knowledge_documents = KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).values(
            "name", "chunk_size", "created_by", "created_at"
        )
        return JsonResponse({"result": True, "data": list(knowledge_documents)})
