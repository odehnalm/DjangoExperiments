import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MaIncident(models.Model):

    _user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)

    reference = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_('Reference')
    )

    record = models.ForeignKey(
        'ma_records.MaRecord',
        related_name='ma_incidents',
        related_query_name="ma_incidents",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = _('Incident MA')
        verbose_name_plural = _('Incidents MA')

    def __str__(self):
        return "%s %s" % (self.reference, self.record.user.get_full_name())
