from django.db import models
from django.utils.translation import gettext_lazy as _
from elasticsearch import NotFoundError

from apps.core.logger import logger
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.core.utils.elasticsearch_utils import get_es_client


class DocumentStatus(object):
    TRAINING = 0
    READY = 1
    ERROR = 2

    CHOICE = (
        (TRAINING, _("Training")),
        (READY, _("Ready")),
        (ERROR, _("Error")),
    )


class KnowledgeDocument(MaintainerInfo, TimeInfo):
    knowledge_base = models.ForeignKey("KnowledgeBase", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    chunk_size = models.IntegerField(default=0, verbose_name=_("分片数"))
    train_status = models.IntegerField(default=0, choices=DocumentStatus.CHOICE, verbose_name="状态")
    train_progress = models.FloatField(default=0, verbose_name="训练进度")
    enable_general_parse = models.BooleanField(default=True, verbose_name="分块解析")
    general_parse_chunk_size = models.IntegerField(default=256, verbose_name="分块大小")
    general_parse_chunk_overlap = models.IntegerField(default=32, verbose_name="分块重叠")
    enable_semantic_chunk_parse = models.BooleanField(default=False, verbose_name="语义分块解析")
    semantic_chunk_parse_embedding_model = models.ForeignKey(
        "model_provider_mgmt.EmbedProvider", blank=True, null=True, on_delete=models.CASCADE, verbose_name="嵌入模型"
    )
    enable_ocr_parse = models.BooleanField(default=False, verbose_name="启用OCR解析")
    ocr_model = models.ForeignKey(
        "model_provider_mgmt.OCRProvider", blank=True, null=True, on_delete=models.CASCADE, verbose_name="OCR模型"
    )
    enable_excel_parse = models.BooleanField(default=True, verbose_name="启用Excel解析")
    excel_header_row_parse = models.BooleanField(default=False, verbose_name="Excel表头+行组合解析")
    excel_full_content_parse = models.BooleanField(default=True, verbose_name="Excel全内容解析")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        index_name = self.knowledge_base.knowledge_index_name()
        es_client = get_es_client()
        try:
            es_client.indices.delete(index=index_name)
            logger.info(f"Index {index_name} successfully deleted.")
        except NotFoundError:
            logger.info(f"Index {index_name} not found, skipping deletion.")

        return super().delete(*args, **kwargs)  # 调用父类的delete方法来执行实际的删除操作

    class Meta:
        verbose_name = _("Knowledge Document")
        verbose_name_plural = verbose_name
