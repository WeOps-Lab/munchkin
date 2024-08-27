from rest_framework import serializers

from apps.knowledge_base.models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = "__all__"
