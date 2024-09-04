from rest_framework import serializers
from rest_framework.fields import empty

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.knowledge_mgmt.models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()

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

    def get_team_name(self, instance: KnowledgeBase):
        return self.group_map.get(instance.team, "")
