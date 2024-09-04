from django.db import models
from django.utils.translation import gettext_lazy as _


class WebPageKnowledge(models.Model):
    url = models.URLField(verbose_name="URL")
    knowledge_document = models.ForeignKey(
        "KnowledgeDocument",
        verbose_name=_("Knowledge Document"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    max_depth = models.IntegerField(verbose_name="最大深度", default=1)

    class Meta:
        verbose_name = _("Web Page Knowledge")
        verbose_name_plural = verbose_name
