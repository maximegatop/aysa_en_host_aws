# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0010_auto_20220726_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='ciclo',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='clase_actividad',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='estado',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='itinerario',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='numero_ruta',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='tipo_orden',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
