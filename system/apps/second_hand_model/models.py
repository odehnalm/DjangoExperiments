import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SecondHandResult(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    value = models.FloatField(verbose_name=_('Value Second Hand'))

    parent = models.ForeignKey(
        settings.REPARATION_SECOND_HAND_PARENT_MODEL,
        related_name='reparation_sh_results',
        related_query_name="reparation_sh_results",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Calculation Second Hand ML')
        verbose_name_plural = _('Calculations Second Hand ML')

    def __str__(self):
        return "Valor ML segunda mano de: "
