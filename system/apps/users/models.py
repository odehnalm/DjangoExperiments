# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, first_name, last_name, username, email,
                     password, is_staff, is_superuser, **extra_fields):

        email = self.normalize_email(email)
        if not email:
            raise ValueError(_(u'The email is required'))
        user = self.model(
            first_name=first_name, last_name=last_name, email=email,
            is_active=True, is_staff=is_staff,
            is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None,
                    first_name='', last_name='', **extra_fields):
        return self._create_user(first_name, last_name, username, email, password, False,
                                 False, **extra_fields)

    def create_superuser(self, username, email, password=None,
                         first_name='', last_name='', **extra_fields):
        return self._create_user(first_name, last_name, username, email, password, True,
                                 True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    _user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)

    # Primer nombre
    first_name = models.CharField(
        max_length=40,
        blank=True
    )

    # Primer apellido (Paterno)
    last_name = models.CharField(
        max_length=40,
        blank=True
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        null=True
    )

    # Correo electrónico
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('This email is not registered'),
        })

    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    EMAIL_NAME = 'email'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email + " - " + self.get_full_name()

    def get_short_name(self):
        return self.first_name

    def get_user_id(self):
        return self._user_id

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def set_email(self, email):
        self.email = email

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    @classmethod
    def get_first_name_string_var(self):
        return self.FIRST_NAME

    @classmethod
    def get_last_name_string_var(self):
        return self.LAST_NAME

    @classmethod
    def get_email_string_var(self):
        return self.EMAIL_NAME

    class Meta:
        ordering = ('email',)
