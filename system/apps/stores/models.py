import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .import choices


class Store(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    store_id = models.CharField(
        max_length=6,
        choices=choices.STORES_CHOICES,
        default=choices.STORES_CHOICES[0][0],
        verbose_name=_('Store ID')
    )

    country = models.CharField(
        max_length=2,
        choices=choices.COUNTRIES_CHOICES,
        default=choices.COUNTRIES_CHOICES[0][0],
        verbose_name=_('Country')
    )

    nombre = models.CharField(
        max_length=200,
        verbose_name=_('Store name')
    )

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return self.nombre
