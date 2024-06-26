# Generated by Django 4.2.7 on 2024-05-28 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model_provider_mgmt', '0001_initial'),
        ('knowledge_mgmt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgebasefolder',
            name='embed_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model_provider_mgmt.embedprovider', verbose_name='嵌入模型'),
        ),
        migrations.AddField(
            model_name='fileknowledge',
            name='knowledge_base_folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge_mgmt.knowledgebasefolder', verbose_name='知识'),
        ),
    ]
