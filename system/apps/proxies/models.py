from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Proxy(models.Model):

    ip_proxy = models.CharField(
        primary_key=True,
        max_length=31,
        verbose_name=_('Proxy IP')
    )

    websites = models.ManyToManyField(settings.WEBSITES_APP_MODEL)

    class Meta:
        verbose_name = _('Proxy')
        verbose_name_plural = _('Proxies')

    def __str__(self):
        return self.ip_proxy
