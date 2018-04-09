import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from . import choices


class MaProfile(models.Model):

    _profile_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    language = models.CharField(
        max_length=2,
        choices=choices.LANGUAGES_CHOICES,
        default=choices.LANGUAGES_CHOICES[0][0],
        verbose_name=_('Language')
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        related_query_name="profile",
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        'ma_companies.MaCompany',
        related_name='ma_profiles',
        related_query_name="ma_profiles",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _('User Profile MA')
        verbose_name_plural = _('User Profiles MA')

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MaProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
