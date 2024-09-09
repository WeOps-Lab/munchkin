from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class KnowledgeBase(MaintainerInfo, TimeInfo):
    name = models.CharField(max_length=100, unique=True)
    introduction = models.TextField(blank=True, null=True)
    team = models.CharField(max_length=100, db_index=True)
    embed_model = models.ForeignKey(
        "model_provider_mgmt.EmbedProvider",
        on_delete=models.CASCADE,
        verbose_name=_("Embed Model"),
        blank=True,
        null=True,
    )
    enable_vector_search = models.BooleanField(
        default=True,
        verbose_name=_("Enable Vector Search"),
    )
    vector_search_weight = models.FloatField(default=0.1, verbose_name=_("Vector Search weight"))
    enable_text_search = models.BooleanField(default=True, verbose_name=_("Enable Text Search"))
    text_search_weight = models.FloatField(default=0.9, verbose_name=_("Text Search Weight"))
    enable_rerank = models.BooleanField(default=True, verbose_name=_("Enable Rerank"))
    rerank_model = models.ForeignKey(
        "model_provider_mgmt.RerankProvider",
        on_delete=models.CASCADE,
        verbose_name=_("Rerank Model"),
        blank=True,
        null=True,
    )

    def knowledge_index_name(self):
        return f"knowledge_base_{self.id}"
