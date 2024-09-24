from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import empty

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.knowledge_mgmt.tasks import retrain_all


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    is_training = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeBase
        fields = "__all__"

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        request = self.context["request"]
        if not hasattr(request, "user"):
            token = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[-1]
            client = KeyCloakClient()
            _, user_info = client.token_is_valid(token)
            groups = client.get_user_groups(user_info["sub"], "admin" in user_info["realm_access"]["roles"])
        else:
            groups = request.user.group_list
        self.group_map = {i["id"]: i["name"] for i in groups}
        self.training_document = list(
            KnowledgeDocument.objects.filter(train_status=DocumentStatus.TRAINING)
            .values_list("knowledge_base_id", flat=True)
            .distinct()
        )

    def get_team_name(self, instance: KnowledgeBase):
        return [self.group_map.get(i) for i in instance.team if i in self.group_map]

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
