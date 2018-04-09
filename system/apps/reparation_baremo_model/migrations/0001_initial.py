# Generated by Django 2.0 on 2018-03-21 15:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReparationBaremoResult',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.FloatField(null=True, verbose_name='Baremo Value')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reparation_baremo_results', related_query_name='reparation_baremo_results', to='tasks.Job')),
            ],
            options={
                'verbose_name': 'Calculation by Scale',
                'verbose_name_plural': 'Calculations by Scale',
            },
        ),
    ]
