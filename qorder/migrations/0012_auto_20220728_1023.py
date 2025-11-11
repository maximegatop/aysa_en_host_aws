# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0011_auto_20220727_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='ciclo',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='clase_actividad',
            field=models.CharField(blank=True, null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='estado',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='itinerario',
            field=models.CharField(blank=True, null=True, max_length=15),
        ),
    ]
