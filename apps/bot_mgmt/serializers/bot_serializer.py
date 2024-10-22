from apps.bot_mgmt.models import Bot
from apps.channel_mgmt.serializers import ChannelSerializer
from config.drf.serializers import TeamSerializer


class BotSerializer(TeamSerializer):
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Bot
        fields = "__all__"
