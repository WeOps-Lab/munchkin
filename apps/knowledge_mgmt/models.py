from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

from apps.embed_mgmt.models import EmbedProvider

TRAIN_STATUS_CHOICES = [
    (0, '待训练'),
    (1, '处理中'),
    (2, '完成'),
    (3, '失败'),
]


class KnowledgeBaseFolder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='知识库名称')
    description = models.TextField(verbose_name='知识库描述')
    embed_model = models.ForeignKey(EmbedProvider, on_delete=models.CASCADE, verbose_name='嵌入模型')
    train_status = models.IntegerField(default=0, choices=TRAIN_STATUS_CHOICES, verbose_name='训练状态')
    train_progress = models.FloatField(default=0, verbose_name='训练进度')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = verbose_name


KNKOWLEDGE_TYPES = ['md', 'docx', 'xlsx', 'csv', 'pptx', 'pdf', 'txt']


class Knowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='文件名称')
    file = models.FileField(verbose_name="文件",
                            storage=MinioBackend(bucket_name='munchkin-private'),
                            upload_to=iso_date_prefix,
                            validators=[FileExtensionValidator(allowed_extensions=KNKOWLEDGE_TYPES)])
    knowledge_base_folder = models.ForeignKey(KnowledgeBaseFolder, verbose_name='知识', blank=True, null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.file.name
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "知识"
        verbose_name_plural = verbose_name
