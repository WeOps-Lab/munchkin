from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import empty

from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.knowledge_mgmt.tasks import retrain_all
from config.drf.serializers import TeamSerializer


class KnowledgeBaseSerializer(TeamSerializer):
    is_training = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeBase
        fields = "__all__"

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.training_document = list(
            KnowledgeDocument.objects.filter(train_status=DocumentStatus.TRAINING)
            .values_list("knowledge_base_id", flat=True)
            .distinct()
        )

    def get_is_training(self, instance: KnowledgeBase):
        return instance.id in self.training_document

    def update(self, instance: KnowledgeBase, validated_data):
        if instance.embed_model_id != validated_data["embed_model"]:
            if instance.knowledgedocument_set.filter(train_status=DocumentStatus.TRAINING).exists():
                return JsonResponse(
                    {"result": False, "message": _("The knowledge base is training and cannot be modified.")}
                )
            retrain_all.delay(instance.id)
        return super().update(instance, validated_data)
