# Generated by Django 4.2.7 on 2024-11-29 02:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot_mgmt", "0005_conversationtag"),
    ]

    operations = [
        migrations.AddField(
            model_name="botconversationhistory",
            name="citing_knowledge",
            field=models.JSONField(blank=True, default=list, null=True, verbose_name="引用知识"),
        ),
    ]
