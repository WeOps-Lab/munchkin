from rest_framework import serializers

from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from config.drf.serializers import TeamSerializer


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = "__all__"


class LLMSerializer(TeamSerializer):
    class Meta:
        model = LLMSkill
        fields = "__all__"
