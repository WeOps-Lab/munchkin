from django.db import models


class EmbedModelChoices(models.TextChoices):
    FASTEMBED = 'fastembed', 'FastEmbed'


class EmbedProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    embed_model = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name='嵌入模型')
    embed_config = models.JSONField(verbose_name='嵌入配置', blank=True, null=True)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "嵌入模型"
        verbose_name_plural = verbose_name
