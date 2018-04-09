import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MaTempModel(models.Model):

    _ma_temp_model_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    id_model = models.CharField(
        max_length=20,
        verbose_name=_('Model Id')
    )

    name_model = models.CharField(
        max_length=100,
        verbose_name=_('Model Name')
    )

    parent = models.ForeignKey(
        settings.MA_TEMP_MODEL_PARENT,
        related_name='ma_temp_models',
        related_query_name="ma_temp_models",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Temporal Model')
        verbose_name_plural = _('Temporal Models')

    def __str__(self):
        return self.name_model


class MaBrand(models.Model):

    _ma_brand_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_brand = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Brand Id')
    )

    name_brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Brand Name')
    )

    class Meta:
        verbose_name = _('Item Brand')
        verbose_name_plural = _('Item Brands')

    def __str__(self):
        return self.name_brand


class MaItemType(models.Model):

    _ma_item_type_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_item_type = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Item Type Id')
    )

    name_item_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Item Type Name')
    )

    brands = models.ManyToManyField(MaBrand)

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

    def __str__(self):
        return self.name_item_type


class MaModel(models.Model):

    _ma_model_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id_model = models.CharField(
        max_length=20,
        verbose_name=_('Model Id')
    )

    brand = models.ForeignKey(
        MaBrand,
        related_name='ma_models',
        related_query_name="ma_models",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Item Model')
        verbose_name_plural = _('Item Models')

    def __str__(self):
        return self.id_model
