# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qorder', '0029_auto_20170727_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='log_rutas',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('estado', models.CharField(null=True, blank=True, verbose_name='Estado', max_length=100)),
                ('fecha_log', models.DateTimeField(null=True, blank=True)),
                ('observacion', models.CharField(null=True, blank=True, verbose_name='Observacion', max_length=100)),
                ('ruta', models.ForeignKey(to='qorder.Ruta', on_delete=django.db.models.deletion.PROTECT)),
                ('usuario', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'logruta',
                'verbose_name_plural': 'logrutas',
            },
        ),
        migrations.AlterField(
            model_name='terminalportatil',
            name='oficina',
            field=models.ForeignKey(null=True, to='core.WorkUnit', related_name='contratistas', on_delete=django.db.models.deletion.PROTECT, blank=True),
        ),
    ]
