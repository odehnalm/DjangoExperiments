import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .import choices


class Product(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    store_id = models.CharField(max_length=6)
    category_id = models.CharField(
        max_length=10,
        choices=choices.CATEGORIES_CHOICES,
        default=choices.CATEGORIES_CHOICES[0][0],
        verbose_name=_('Category')
    )
    nombre = models.CharField(max_length=200)
    ficha_tecnica = JSONField()
    detalles = JSONField()
    tiendas = JSONField()

    parent = models.ForeignKey(
        settings.SUBSTITUTION_SIMILAR_PARENT_MODEL,
        related_name='substitution_similar_results',
        related_query_name="substitution_similar_results",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Product (Webscraping)')
        verbose_name_plural = _('Products (Webscraping)')

    def __str__(self):
        return self.nombre
