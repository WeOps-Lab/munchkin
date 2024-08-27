from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class KnowledgeBase(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    introduction = models.TextField()
    content = models.TextField()
