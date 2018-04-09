import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MaRecord(models.Model):

    _user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)

    reference = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_('Record')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ma_records',
        related_query_name="ma_records",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = _('Record MA')
        verbose_name_plural = _('Records MA')

    def __str__(self):
        return "%s %s" % (self.reference, self.user.get_full_name())
