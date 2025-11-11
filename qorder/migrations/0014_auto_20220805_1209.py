# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0013_auto_20220801_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fecha_asignacion',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fecha_descarga',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fecha_generacion',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fh_fin',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fh_inicio',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
