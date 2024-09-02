from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeInfo(models.Model):
    """
    Add time fields to another models.
    """

    class Meta:
        verbose_name = _("时间相关字段")
        abstract = True

    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("修改时间"), auto_now=True)
