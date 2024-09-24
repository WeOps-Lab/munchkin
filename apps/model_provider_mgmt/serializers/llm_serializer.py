from rest_framework import serializers

from apps.model_provider_mgmt.models import LLMModel, LLMSkill


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = "__all__"


class LLMSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMSkill
        fields = "__all__"
