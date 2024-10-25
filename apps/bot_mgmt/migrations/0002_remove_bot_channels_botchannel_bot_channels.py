# Generated by Django 4.2.7 on 2024-10-23 09:27

import django.db.models.deletion
import django_yaml_field.fields
from django.db import migrations, models

import apps.core.mixinx


class Migration(migrations.Migration):
    dependencies = [
        ("bot_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bot",
            name="channels",
        ),
        migrations.CreateModel(
            name="BotChannel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "channel_type",
                    models.CharField(
                        choices=[
                            ("enterprise_wechat", "Enterprise WeChat"),
                            ("enterprise_wechat_bot", "Enterprise WeChat Bot"),
                            ("ding_talk", "Ding Talk"),
                            ("web", "Web"),
                            ("gitlab", "GitLab"),
                        ],
                        max_length=100,
                        verbose_name="channel type",
                    ),
                ),
                (
                    "channel_config",
                    django_yaml_field.fields.YAMLField(blank=True, null=True, verbose_name="channel config"),
                ),
                ("enabled", models.BooleanField(default=False, verbose_name="enabled")),
                (
                    "bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bot_mgmt.bot", verbose_name="机器人"
                    ),
                ),
            ],
            bases=(models.Model, apps.core.mixinx.EncryptMixin),
        ),
        migrations.AddField(
            model_name="bot",
            name="channels",
            field=models.JSONField(default=list),
        ),
    ]