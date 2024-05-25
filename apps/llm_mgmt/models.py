from django.db import models


class EmbedModelChoices(models.TextChoices):
    FASTEMBED = 'fastembed', 'FastEmbed'


class LLMModelChoices(models.TextChoices):
    GPT35_16K = 'gpt-3.5-turbo-16k', 'GPT-3.5 Turbo 16K'


class LLMModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.CharField(max_length=255, choices=LLMModelChoices.choices, verbose_name='LLM模型')
    llm_config = models.JSONField(verbose_name='LLM配置', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLM模型"
        verbose_name_plural = verbose_name


class EmbedProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    embed_model = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name='嵌入模型')
    embed_config = models.JSONField(verbose_name='嵌入配置', blank=True, null=True)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
