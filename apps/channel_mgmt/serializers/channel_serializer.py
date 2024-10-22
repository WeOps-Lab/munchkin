from rest_framework import serializers

from apps.channel_mgmt.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["channel_config"] = instance.format_channel_config()
        return response
