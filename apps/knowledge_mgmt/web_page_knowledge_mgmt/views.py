from apps.knowledge_mgmt.models import WebPageKnowledge
from apps.knowledge_mgmt.viewset_utils import AuthViewSet
from apps.knowledge_mgmt.web_page_knowledge_mgmt.serializers import WebPageKnowledgeSerializer


class WebPageKnowledgeViewSet(AuthViewSet):
    queryset = WebPageKnowledge.objects.all()
    serializer_class = WebPageKnowledgeSerializer
    ordering = ("-id",)
    search_fields = ("name",)
