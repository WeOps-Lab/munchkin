from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.knowledge_base.enums import DocumentStatus, SourceType


class KnowledgeBase(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=100, db_index=True)
    team = models.CharField(max_length=100)
    introduction = models.TextField(blank=True, null=True)


class KnowledgeDocument(MaintainerInfo, TimeInfo):
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    status = models.CharField(max_length=15, choices=DocumentStatus.CHOICE, default=DocumentStatus.TRAINING)
    source_type = models.CharField(max_length=25, choices=SourceType.CHOICE, default=SourceType.LOCAL)
    doc_data = models.JSONField(default=dict)
    chunk_size = models.IntegerField(default=0)
