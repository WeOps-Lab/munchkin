# Generated by Django 4.2.7 on 2024-10-10 09:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.core.encoders
import apps.core.mixinx


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("knowledge_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmbedProvider",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="名称")),
                (
                    "embed_model_type",
                    models.CharField(choices=[("lang-serve", "LangServe")], max_length=255, verbose_name="嵌入模型"),
                ),
                (
                    "embed_config",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=apps.core.encoders.PrettyJSONEncoder,
                        null=True,
                        verbose_name="嵌入配置",
                    ),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="是否启用")),
            ],
            options={
                "verbose_name": "Embed模型",
                "verbose_name_plural": "Embed模型",
            },
            bases=(models.Model, apps.core.mixinx.EncryptMixin),
        ),
        migrations.CreateModel(
            name="LLMModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="名称")),
                (
                    "llm_model_type",
                    models.CharField(
                        choices=[("chat-gpt", "ChatGPT"), ("zhipu", "智谱AI")], max_length=255, verbose_name="LLM模型类型"
                    ),
                ),
                (
                    "llm_config",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=apps.core.encoders.PrettyJSONEncoder,
                        null=True,
                        verbose_name="LLM配置",
                    ),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="启用")),
            ],
            options={
                "verbose_name": "LLM模型",
                "verbose_name_plural": "LLM模型",
            },
            bases=(models.Model, apps.core.mixinx.EncryptMixin),
        ),
        migrations.CreateModel(
            name="OCRProvider",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="名称")),
                ("ocr_config", models.JSONField(blank=True, default=dict, null=True, verbose_name="OCR配置")),
                ("enabled", models.BooleanField(default=True, verbose_name="是否启用")),
            ],
            options={
                "verbose_name": "OCR模型",
                "verbose_name_plural": "OCR模型",
            },
        ),
        migrations.CreateModel(
            name="RerankProvider",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="名称")),
                (
                    "rerank_model_type",
                    models.CharField(choices=[("langserve", "LangServe")], max_length=255, verbose_name="模型类型"),
                ),
                (
                    "rerank_config",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=apps.core.encoders.PrettyJSONEncoder,
                        null=True,
                        verbose_name="Rerank配置",
                    ),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="是否启用")),
            ],
            options={
                "verbose_name": "Rerank模型",
                "verbose_name_plural": "Rerank模型",
            },
            bases=(models.Model, apps.core.mixinx.EncryptMixin),
        ),
        migrations.CreateModel(
            name="LLMSkill",
            fields=[
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, verbose_name="名称")),
                ("skill_id", models.CharField(blank=True, max_length=255, null=True, verbose_name="技能ID")),
                ("skill_prompt", models.TextField(blank=True, null=True, verbose_name="技能提示词")),
                ("enable_conversation_history", models.BooleanField(default=False, verbose_name="启用对话历史")),
                ("conversation_window_size", models.IntegerField(default=10, verbose_name="对话窗口大小")),
                ("enable_rag", models.BooleanField(default=False, verbose_name="启用RAG")),
                ("enable_rag_knowledge_source", models.BooleanField(default=False, verbose_name="显示RAG知识来源")),
                ("rag_score_threshold_map", models.JSONField(default=dict, verbose_name="知识库RAG分数阈值映射")),
                ("introduction", models.TextField(blank=True, default="", null=True, verbose_name="介绍")),
                ("team", models.JSONField(default=list, verbose_name="分组")),
                ("temperature", models.FloatField(default=0.7, verbose_name="温度")),
                (
                    "knowledge_base",
                    models.ManyToManyField(blank=True, to="knowledge_mgmt.knowledgebase", verbose_name="知识库"),
                ),
                (
                    "llm_model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="model_provider_mgmt.llmmodel",
                        verbose_name="LLM模型",
                    ),
                ),
            ],
            options={
                "verbose_name": "LLM技能管理",
                "verbose_name_plural": "LLM技能管理",
            },
        ),
        migrations.AddConstraint(
            model_name="llmskill",
            constraint=models.UniqueConstraint(fields=("created_by", "name"), name="unique_owner_name"),
        ),
    ]
