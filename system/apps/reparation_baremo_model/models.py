import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ReparationBaremoResult(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    value = models.FloatField(
        null=True,
        verbose_name=_('Baremo Value'))

    parent = models.ForeignKey(
        settings.REPARATION_BAREMO_PARENT_MODEL,
        related_name='reparation_baremo_results',
        related_query_name="reparation_baremo_results",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Calculation by Scale')
        verbose_name_plural = _('Calculations by Scale')

    def __str__(self):
        return "Valor reparacion por Baremo de: "
