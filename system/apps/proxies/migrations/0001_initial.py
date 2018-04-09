# Generated by Django 2.0 on 2018-03-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('ip_proxy', models.CharField(max_length=31, primary_key=True, serialize=False, verbose_name='Proxy IP')),
                ('websites', models.ManyToManyField(to='stores.Store')),
            ],
            options={
                'verbose_name': 'Proxy',
                'verbose_name_plural': 'Proxies',
            },
        ),
    ]
