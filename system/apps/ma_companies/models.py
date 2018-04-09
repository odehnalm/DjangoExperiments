import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import choices


class MaCompany(models.Model):

    _user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)

    name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_('Name Company')
    )

    country = models.CharField(
        max_length=2,
        choices=choices.COUNTRIES_CHOICES,
        default=choices.COUNTRIES_CHOICES[0][0],
        verbose_name=_('Country')
    )

    # Vinculo a usuarios de una compania
    ma_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ma_profiles.MaProfile'
    )

    class Meta:
        verbose_name = _('Company MA')
        verbose_name_plural = _('Companies MA')

    def __str__(self):
        return self.name
