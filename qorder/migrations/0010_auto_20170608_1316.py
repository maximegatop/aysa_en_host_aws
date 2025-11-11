# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0009_historicoconsumo_tipo_consumo'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodesuministro',
            name='Frecuencia',
            field=models.CharField(verbose_name='Frecuencia', blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='puntodesuministro',
            name='rutasum2',
            field=models.ForeignKey(to='qorder.RutaSum', blank=True, null=True, related_name='rutasum2', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='puntodesuministro',
            name='secuencia_teorica2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rutasum',
            name='Frecuencia',
            field=models.CharField(verbose_name='Frecuencia', blank=True, max_length=10, null=True),
        ),
    ]
