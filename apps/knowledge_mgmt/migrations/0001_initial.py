# Generated by Django 4.2.7 on 2024-09-04 07:51

import django.core.validators
import django.db.models.deletion
import django_minio_backend.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FileKnowledge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "file",
                    models.FileField(
                        storage=django_minio_backend.models.MinioBackend(bucket_name="munchkin-private"),
                        upload_to=django_minio_backend.models.iso_date_prefix,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "md",
                                    "docx",
                                    "xlsx",
                                    "csv",
                                    "pptx",
                                    "pdf",
                                    "txt",
                                    "png",
                                    "jpg",
                                    "jpeg",
                                ]
                            )
                        ],
                        verbose_name="文件",
                    ),
                ),
            ],
            options={
                "verbose_name": "File Knowledge",
                "verbose_name_plural": "File Knowledge",
            },
        ),
        migrations.CreateModel(
            name="KnowledgeBase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="创建者")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="更新者")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("introduction", models.TextField(blank=True, null=True)),
                ("team", models.CharField(db_index=True, max_length=100)),
                ("enable_vector_search", models.BooleanField(default=True, verbose_name="向量检索")),
                ("vector_search_weight", models.FloatField(default=0.1, verbose_name="向量检索权重")),
                ("enable_text_search", models.BooleanField(default=True, verbose_name="文本检索")),
                ("text_search_weight", models.FloatField(default=0.9, verbose_name="文本检索权重")),
                ("enable_rerank", models.BooleanField(default=True, verbose_name="启用Rerank")),
            ],
            options={
                "verbose_name": "维护者相关字段",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KnowledgeDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="修改时间")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="创建者")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="更新者")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="名称")),
                ("chunk_size", models.IntegerField(default=0, verbose_name="分片数")),
                (
                    "train_status",
                    models.IntegerField(
                        choices=[(0, "Training"), (1, "Ready"), (2, "Error")], default=0, verbose_name="状态"
                    ),
                ),
                ("train_progress", models.FloatField(default=0, verbose_name="训练进度")),
                ("enable_general_parse", models.BooleanField(default=True, verbose_name="分块解析")),
                ("general_parse_chunk_size", models.IntegerField(default=256, verbose_name="分块大小")),
                ("general_parse_chunk_overlap", models.IntegerField(default=32, verbose_name="分块重叠")),
                ("enable_semantic_chunk_parse", models.BooleanField(default=False, verbose_name="语义分块解析")),
                ("enable_ocr_parse", models.BooleanField(default=False, verbose_name="启用OCR解析")),
                ("excel_header_row_parse", models.BooleanField(default=False, verbose_name="Excel表头+行组合解析")),
                ("excel_full_content_parse", models.BooleanField(default=True, verbose_name="Excel全内容解析")),
                (
                    "knowledge_base",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="knowledge_mgmt.knowledgebase"),
                ),
            ],
            options={
                "verbose_name": "Knowledge Document",
                "verbose_name_plural": "Knowledge Document",
            },
        ),
        migrations.CreateModel(
            name="WebPageKnowledge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("url", models.URLField(verbose_name="URL")),
                ("max_depth", models.IntegerField(default=1, verbose_name="最大深度")),
                (
                    "knowledge_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="knowledge_mgmt.knowledgedocument",
                        verbose_name="Knowledge Document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Web Page Knowledge",
                "verbose_name_plural": "Web Page Knowledge",
            },
        ),
        migrations.CreateModel(
            name="ManualKnowledge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "knowledge_document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="knowledge_mgmt.knowledgedocument",
                        verbose_name="Knowledge Document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Manual Knowledge",
                "verbose_name_plural": "Manual Knowledge",
            },
        ),
    ]
