from django.db import models

from apps.channel_mgmt.models import Channel
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.llm_mgmt.models import LLMModel


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    channels = models.ManyToManyField(Channel, verbose_name='通道')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机器人'
        verbose_name_plural = verbose_name


class BotSkill(models.Model):
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name='机器人')
    name = models.CharField(max_length=255, verbose_name='技能名称')
    skill_id = models.CharField(max_length=255, verbose_name='技能ID', default='')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    llm_model = models.ForeignKey(LLMModel, on_delete=models.CASCADE, verbose_name='LLM模型')
    skill_prompt = models.TextField(blank=True, null=True, verbose_name='技能提示词')

    enable_conversation_history = models.BooleanField(default=False, verbose_name='启用对话历史')
    conversation_window_size = models.IntegerField(default=10, verbose_name='对话窗口大小')

    enable_rag = models.BooleanField(default=False, verbose_name='启用RAG')
    knowledge_base_folders = models.ManyToManyField(KnowledgeBaseFolder, null=True, blank=True, verbose_name='知识库')
    rag_top_k = models.IntegerField(default=5, verbose_name='RAG返回结果数量')
    rag_num_candidates = models.IntegerField(default=1000, verbose_name='RAG向量候选数量')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机器人技能'
        verbose_name_plural = verbose_name


class BotSkillRule(models.Model):
    id = models.AutoField(primary_key=True)
    bot_skill = models.ForeignKey(BotSkill, on_delete=models.CASCADE, verbose_name='技能')
    name = models.CharField(max_length=255, verbose_name='规则名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    prompt = models.TextField(blank=True, null=True, verbose_name='技能提示词')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '规则'
        verbose_name_plural = verbose_name
