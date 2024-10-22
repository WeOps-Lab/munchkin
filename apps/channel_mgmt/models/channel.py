from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_yaml_field import YAMLField

from apps.core.mixinx import EncryptMixin
from apps.core.models.maintainer_info import MaintainerInfo


class ChannelChoices(models.TextChoices):
    ENTERPRISE_WECHAT = ("enterprise_wechat", _("Enterprise WeChat"))
    ENTERPRISE_WECHAT_BOT = ("enterprise_wechat_bot", _("Enterprise WeChat Bot"))
    DING_TALK = ("ding_talk", _("Ding Talk"))
    WEB = ("web", _("Web"))
    GITLAB = ("gitlab", _("GitLab"))


class Channel(MaintainerInfo, EncryptMixin):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    channel_type = models.CharField(max_length=100, choices=ChannelChoices.choices, verbose_name=_("channel type"))
    channel_config = YAMLField(verbose_name=_("channel config"), blank=True, null=True)
    enabled = models.BooleanField(default=False, verbose_name=_("enabled"))

    def save(self, *args, **kwargs):
        if self.channel_config is None:
            super(Channel, self).save()
        if self.channel_type == ChannelChoices.GITLAB:
            self.encrypt_field(
                "secret_token", self.channel_config["channels.gitlab_review_channel.GitlabReviewChannel"]
            )

        elif self.channel_type == ChannelChoices.DING_TALK:
            self.encrypt_field("client_secret", self.channel_config["channels.dingtalk_channel.DingTalkChannel"])

        elif self.channel_type == ChannelChoices.ENTERPRISE_WECHAT:
            self.encrypt_field(
                "secret_token", self.channel_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )
            self.encrypt_field(
                "aes_key", self.channel_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )
            self.encrypt_field(
                "secret", self.channel_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )
            self.encrypt_field(
                "token", self.channel_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )

        elif self.channel_type == ChannelChoices.ENTERPRISE_WECHAT_BOT:
            self.encrypt_field(
                "secret_token",
                self.channel_config["channels.enterprise_wechat_bot_channel.EnterpriseWechatBotChannel"],
            )

        super().save(*args, **kwargs)

    @cached_property
    def decrypted_channel_config(self):
        decrypted_config = self.channel_config.copy()
        if self.channel_type == ChannelChoices.GITLAB:
            self.decrypt_field("secret_token", decrypted_config["channels.gitlab_review_channel.GitlabReviewChannel"])

        if self.channel_type == ChannelChoices.DING_TALK:
            self.decrypt_field("client_secret", decrypted_config["channels.dingtalk_channel.DingTalkChannel"])

        elif self.channel_type == ChannelChoices.ENTERPRISE_WECHAT:
            self.decrypt_field(
                "secret_token", decrypted_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )
            self.decrypt_field(
                "aes_key", decrypted_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
            )
            self.decrypt_field("secret", decrypted_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"])
            self.decrypt_field("token", decrypted_config["channels.enterprise_wechat_channel.EnterpriseWechatChannel"])

        elif self.channel_type == ChannelChoices.ENTERPRISE_WECHAT_BOT:
            self.decrypt_field(
                "secret_token", decrypted_config["channels.enterprise_wechat_bot_channel.EnterpriseWechatBotChannel"]
            )

        return decrypted_config

    class Meta:
        verbose_name = _("channel")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def format_channel_config(self):
        return_data = {}
        keys = ["secret", "token", "aes_key", "client_secret"]
        for key, value in self.channel_config.items():
            return_data[key] = {i: "******" if v and i in keys else v for i, v in value.items()}
        return return_data
