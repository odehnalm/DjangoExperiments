import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import choices


class Item(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    store = models.ForeignKey(
        settings.WEBSITES_APP_MODEL,
        related_name='items',
        related_query_name="items",
        on_delete=models.SET_NULL,
        null=True
    )

    category_id = models.CharField(
        max_length=10,
        choices=choices.CATEGORIES_CHOICES,
        default=choices.CATEGORIES_CHOICES[0][0],
        verbose_name=_('Category')
    )

    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.nombre
