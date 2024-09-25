# Generated by Django 4.2.7 on 2024-09-24 05:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("model_provider_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="llmskill",
            name="groups",
            field=models.JSONField(default=list, verbose_name="分组"),
        ),
        migrations.AddField(
            model_name="llmskill",
            name="introduction",
            field=models.TextField(blank=True, default="", null=True, verbose_name="介绍"),
        ),
        migrations.AlterField(
            model_name="llmskill",
            name="created_by",
            field=models.CharField(default="", max_length=32, verbose_name="Creator"),
        ),
        migrations.AlterField(
            model_name="llmskill",
            name="updated_by",
            field=models.CharField(default="", max_length=32, verbose_name="Updater"),
        ),
    ]