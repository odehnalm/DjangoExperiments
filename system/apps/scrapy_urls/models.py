import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UrlGenerated(models.Model):

    _id = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)

    url = models.URLField(max_length=3000)

    parent = models.ForeignKey(
        settings.SCRAPY_URLS_PARENT_MODEL,
        related_name='urls_generated',
        related_query_name="urls_generated",
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = _('Url (Webcraping)')
        verbose_name_plural = _('Urls (Webcraping)')

    def __str__(self):
        return "Urls generadas para webscraping"
