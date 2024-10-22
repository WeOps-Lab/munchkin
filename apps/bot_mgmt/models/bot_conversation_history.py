from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo

BOT_CONVERSATION_ROLE_CHOICES = [("user", "用户"), ("bot", "机器人")]


class BotConversationHistory(MaintainerInfo):
    bot = models.ForeignKey("bot_mgmt.Bot", on_delete=models.CASCADE, verbose_name="机器人")
    user_info = models.JSONField(verbose_name="用户信息", default=dict)
    conversation_role = models.CharField(max_length=255, verbose_name="对话角色", choices=BOT_CONVERSATION_ROLE_CHOICES)
    conversation = models.TextField(verbose_name="对话内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.conversation

    class Meta:
        verbose_name = "对话历史"
        verbose_name_plural = verbose_name
