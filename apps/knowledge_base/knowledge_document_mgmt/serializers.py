from rest_framework import serializers

from apps.knowledge_base.models import KnowledgeDocument


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = "__all__"
