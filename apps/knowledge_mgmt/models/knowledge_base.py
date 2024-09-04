from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class KnowledgeBase(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=100, unique=True)
    introduction = models.TextField(blank=True, null=True)
    team = models.CharField(max_length=100, db_index=True)
    embed_model = models.ForeignKey(
        "model_provider_mgmt.EmbedProvider",
        on_delete=models.CASCADE,
        verbose_name="嵌入模型",
        blank=True,
        null=True,
    )
    enable_vector_search = models.BooleanField(default=True, verbose_name="向量检索")
    vector_search_weight = models.FloatField(default=0.1, verbose_name="向量检索权重")
    enable_text_search = models.BooleanField(default=True, verbose_name="文本检索")
    text_search_weight = models.FloatField(default=0.9, verbose_name="文本检索权重")
    enable_rerank = models.BooleanField(default=True, verbose_name="启用Rerank")
    rerank_model = models.ForeignKey(
        "model_provider_mgmt.RerankProvider",
        on_delete=models.CASCADE,
        verbose_name="Rerank模型",
        blank=True,
        null=True,
    )

    def knowledge_index_name(self):
        return f"knowledge_base_{self.id}"
