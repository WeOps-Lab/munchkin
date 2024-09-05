from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from rest_framework.decorators import action

from apps.knowledge_mgmt.knowledge_document_mgmt.serializers import KnowledgeDocumentSerializer
from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class KnowledgeDocumentViewSet(AuthViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    ordering = ("-id",)
    search_fields = ("name", "knowledge_source_type")

    @action(methods=["POST"], detail=False)
    def preprocess(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        knowledge_base_id = kwargs.pop("knowledge_base_id")
        source_type = kwargs.pop("knowledge_source_type")
        KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(**kwargs)
        doc_list = KnowledgeDocumentUtils.general_embed_by_document_list(
            knowledge_document_ids, knowledge_base_id, source_type
        )
        return JsonResponse({"result": True, "data": doc_list})

    @action(methods=["post"], detail=False)
    def search(self, request):
        data = request.data
        knowledge_base_id = data.get("knowledge_base_id")
        query = data.get("query")
        metadata = data.get("metadata", {})
        score_threshold = data.get("score_threshold", 0)
        page = data.get("page", 1)
        size = data.get("size", 10)
        start = (page - 1) * size  # 计算开始的记录
        ordering = data.get("ordering", "-created_at")
        if query:
            service = KnowledgeSearchService()
            knowledge_base = KnowledgeBase.objects.filter(id=knowledge_base_id)
            docs = service.search(knowledge_base, query, metadata, score_threshold)
            doc_ids = [doc["knowledge_id"] for doc in docs]
            knowledge_document_list = KnowledgeDocument.objects.filter(id__in=set(doc_ids))

            # 处理特殊排序score
            if "score" in ordering:
                # 去重同时保持顺序
                seen = set()
                ordered_unique_docs_ids = [x for x in doc_ids if not (x in seen or seen.add(x))]
                # doc_ids默认是按分数从高到底返回, 如果要按score正序则需要逆向ordered_unique_docs_ids顺序
                if "-" not in ordering:
                    ordered_unique_docs_ids.reverse()

                # 构建排序条件
                preserved_order = Case(
                    *[When(pk=pk, then=Value(i)) for i, pk in enumerate(ordered_unique_docs_ids)],
                    output_field=IntegerField()
                )
                ordering = preserved_order
        else:
            knowledge_document_list = KnowledgeDocument.objects.all()

        knowledge_document_list = knowledge_document_list.order_by(ordering)
        total = knowledge_document_list.count()  # 获取总记录数
        manual_knowledge = knowledge_document_list[start : start + size]  # 应用分页

        serializer = KnowledgeDocumentSerializer(manual_knowledge, many=True)
        results = {
            "result": True,
            "data": {
                "count": total,  # 返回总记录数
                "items": serializer.data,
                "page": page,
                "size": size,
                "total_pages": (total + size - 1) // size,  # 计算总页数
            },
        }
        return JsonResponse(results)
