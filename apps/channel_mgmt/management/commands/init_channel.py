from django.core.management import BaseCommand

from apps.bot_mgmt.models import Bot, BotSkill
from apps.channel_mgmt.models import Channel, CHANNEL_CHOICES
from apps.llm_mgmt.models import LLMModel, LLMModelChoices


class Command(BaseCommand):
    help = '初始化消息通道'

    def handle(self, *args, **options):
        Channel.objects.get_or_create(name=CHANNEL_CHOICES.ENTERPRISE_WECHAT.value,
                                      channel_type=CHANNEL_CHOICES.ENTERPRISE_WECHAT,
                                      channel_config={
                                          "corp_id": "",
                                          "secret": "",
                                          "token": "",
                                          "aes_key": "",
                                          "agent_id": "",

                                      })
        Channel.objects.get_or_create(name=CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT.value,
                                      channel_type=CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT,
                                      channel_config={
                                          "enterprise_bot_url": "",
                                          "secret_token": "",
                                          "enable_eventbus": "",
                                      })
        Channel.objects.get_or_create(name=CHANNEL_CHOICES.DING_TALK.value,
                                      channel_type=CHANNEL_CHOICES.DING_TALK,
                                      channel_config={
                                          "client_id": "",
                                          "client_secret": "",
                                          "enable_eventbus": "",
                                      })
        Channel.objects.get_or_create(name=CHANNEL_CHOICES.WEB.value,
                                      channel_type=CHANNEL_CHOICES.WEB,
                                      channel_config={
                                      })
        Channel.objects.get_or_create(name=CHANNEL_CHOICES.GITLAB.value,
                                      channel_type=CHANNEL_CHOICES.GITLAB,
                                      channel_config={
                                          "token": "",
                                          "gitlab_token": "",
                                          "gitlab_url": "",
                                          "secret_token": "",
                                      })
