# Generated by Django 2.0 on 2018-03-21 15:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ma_companies', '0001_initial'),
        ('ma_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='macompany',
            name='ma_users',
            field=models.ManyToManyField(through='ma_profiles.MaProfile', to=settings.AUTH_USER_MODEL),
        ),
    ]
