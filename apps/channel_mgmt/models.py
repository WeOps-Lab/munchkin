from django.db import models

from apps.core.encoders import PrettyJSONEncoder


class CHANNEL_CHOICES(models.TextChoices):
    ENTERPRISE_WECHAT = ('enterprise_wechat', '企业微信')
    ENTERPRISE_WECHAT_BOT = ('enterprise_wechat_bot', '企业微信机器人')
    DING_TALK = ('ding_talk', '钉钉')
    WEB = ('web', 'Web')
    GITLAB = ('gitlab', 'GitLab')


class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='名称')
    channel_type = models.CharField(max_length=100, choices=CHANNEL_CHOICES.choices, verbose_name='类型')
    channel_config = models.JSONField(verbose_name='通道配置', blank=True, null=True, encoder=PrettyJSONEncoder)

    class Meta:
        verbose_name = '消息通道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
