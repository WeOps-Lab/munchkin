from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.knowledge_mgmt.knowledge_document_mgmt.serializers import KnowledgeDocumentSerializer
from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.knowledge_mgmt.tasks import general_embed
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class ObjFilter(FilterSet):
    knowledge_base_id = filters.NumberFilter(field_name="knowledge_base_id", lookup_expr="exact")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    knowledge_source_type = filters.CharFilter(field_name="knowledge_source_type", lookup_expr="exact")
    train_status = filters.NumberFilter(field_name="train_status", lookup_expr="exact")


class KnowledgeDocumentViewSet(AuthViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    filterset_class = ObjFilter
    ordering = ("-id",)

    @action(methods=["POST"], detail=False)
    def preprocess(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        source_type = kwargs.pop("knowledge_source_type")
        preview = kwargs.pop("preview", False)
        KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(**kwargs)
        if preview:
            doc_list = KnowledgeDocumentUtils.general_embed_by_document_list(knowledge_document_ids, source_type)
            return JsonResponse({"result": True, "data": doc_list})
        general_embed.delay(knowledge_document_ids, source_type)
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def testing(self, request):
        kwargs = request.data
        knowledge_base_id = kwargs.pop("knowledge_base_id", 0)
        query = kwargs.pop("query", "")
        if not query:
            return JsonResponse({"result": False, "message": _("query is required")})

        service = KnowledgeSearchService()
        knowledge_base = KnowledgeBase.objects.filter(id=knowledge_base_id)
        docs = service.search(knowledge_base, query, kwargs)
        doc_ids = [doc["knowledge_id"] for doc in docs]
        knowledge_document_list = KnowledgeDocument.objects.filter(id__in=set(doc_ids)).values(
            "id", "name", "knowledge_source_type", "created_by", "created_at"
        )
        seen = set()
        ordered_unique_docs_ids = [x for x in doc_ids if not (x in seen or seen.add(x))]
        # 构建排序条件
        preserved_order = Case(
            *[When(pk=pk, then=Value(i)) for i, pk in enumerate(ordered_unique_docs_ids)], output_field=IntegerField()
        )
        ordering = preserved_order
        knowledge_document_list = knowledge_document_list.order_by(ordering)
        doc_map = {doc["id"]: doc for doc in knowledge_document_list}
        for i in docs:
            doc_obj = doc_map.get(i.pop("knowledge_id"))
            i.update(doc_obj)
        return JsonResponse({"result": True, "data": docs})
