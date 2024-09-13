from rest_framework import serializers

from apps.model_provider_mgmt.models import LLMModel


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = "__all__"
