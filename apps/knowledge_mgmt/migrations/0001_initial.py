# Generated by Django 4.2.7 on 2024-10-10 09:24

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
                        verbose_name="File",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("introduction", models.TextField(blank=True, null=True)),
                ("team", models.JSONField(default=list)),
                ("enable_vector_search", models.BooleanField(default=True, verbose_name="Enable Vector Search")),
                ("vector_search_weight", models.FloatField(default=0.1, verbose_name="Vector Search weight")),
                ("enable_text_search", models.BooleanField(default=True, verbose_name="Enable Text Search")),
                ("text_search_weight", models.FloatField(default=0.9, verbose_name="Text Search Weight")),
                ("enable_rerank", models.BooleanField(default=True, verbose_name="Enable Rerank")),
                ("rag_k", models.IntegerField(default=50, verbose_name="Number of Results")),
                ("rag_num_candidates", models.IntegerField(default=1000, verbose_name="Number of Candidates")),
                ("text_search_mode", models.CharField(default="match", max_length=20, verbose_name="Text search mode")),
            ],
            options={
                "verbose_name": "Maintainer Fields",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KnowledgeDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("name", models.CharField(db_index=True, max_length=255, verbose_name="name")),
                ("chunk_size", models.IntegerField(default=0, verbose_name="chunk size")),
                (
                    "train_status",
                    models.IntegerField(
                        choices=[(0, "Training"), (1, "Ready"), (2, "Error"), (3, "Pending"), (4, "Chunking")],
                        default=0,
                        verbose_name="train status",
                    ),
                ),
                ("train_progress", models.FloatField(default=0, verbose_name="train progress")),
                ("enable_general_parse", models.BooleanField(default=True, verbose_name="enable general parse")),
                ("general_parse_chunk_size", models.IntegerField(default=256, verbose_name="general parse chunk size")),
                (
                    "general_parse_chunk_overlap",
                    models.IntegerField(default=32, verbose_name="general parse chunk overlap"),
                ),
                (
                    "enable_semantic_chunk_parse",
                    models.BooleanField(default=False, verbose_name="enable semantic chunk parse"),
                ),
                ("enable_ocr_parse", models.BooleanField(default=False, verbose_name="enable OCR parse")),
                ("enable_excel_parse", models.BooleanField(default=True, verbose_name="enable Excel parse")),
                ("excel_header_row_parse", models.BooleanField(default=False, verbose_name="Excel header row parse")),
                (
                    "excel_full_content_parse",
                    models.BooleanField(default=True, verbose_name="Excel full content parse"),
                ),
                ("knowledge_source_type", models.CharField(default="file", max_length=20, verbose_name="source type")),
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
                ("max_depth", models.IntegerField(default=1, verbose_name="max depth")),
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
                ("content", models.TextField(verbose_name="content")),
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
