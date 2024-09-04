# Generated by Django 4.2.7 on 2024-09-03 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("knowledge_mgmt", "0001_initial"),
        ("model_provider_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="knowledgebase",
            name="embed_model",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="model_provider_mgmt.embedprovider", verbose_name="嵌入模型"
            ),
        ),
        migrations.AddField(
            model_name="knowledgebase",
            name="rerank_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="model_provider_mgmt.rerankprovider",
                verbose_name="Rerank模型",
            ),
        ),
        migrations.AddField(
            model_name="fileknowledge",
            name="knowledge_document",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="knowledge_mgmt.knowledgedocument",
                verbose_name="Knowledge Document",
            ),
        ),
    ]
