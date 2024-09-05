from rest_framework import serializers

from apps.knowledge_mgmt.models import KnowledgeDocument


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = "__all__"

    def __init__(self, instance, **kwargs):
        super(KnowledgeDocumentSerializer, self).__init__(instance, **kwargs)
