import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ReparationMLResult(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    value = models.IntegerField()

    parent = models.ForeignKey(
        settings.REPARATION_ML_PARENT_MODEL,
        related_name='reparation_ml_results',
        related_query_name="reparation_ml_results",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Calculation by ML')
        verbose_name_plural = _('Calculations by ML')

    def __str__(self):
        return "Valor ML reparacion de: "
