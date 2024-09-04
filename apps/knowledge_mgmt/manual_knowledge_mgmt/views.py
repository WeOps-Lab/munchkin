from apps.knowledge_mgmt.manual_knowledge_mgmt.serializers import ManualKnowledgeSerializer
from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.viewset_utils import AuthViewSet


class ManualKnowledgeViewSet(AuthViewSet):
    queryset = ManualKnowledge.objects.all()
    serializer_class = ManualKnowledgeSerializer
    ordering = ("-id",)
    search_fields = ("name",)
