# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0005_auto_20170328_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='desc_lectura',
            name='lecturas_ingresadas',
            field=models.CharField(null=True, verbose_name='lecturas ingresadas', max_length=250, blank=True),
        ),
        migrations.AddField(
            model_name='ruta',
            name='fecha_hora_exportacion',
            field=models.CharField(null=True, max_length=14, blank=True),
        ),
        migrations.AddField(
            model_name='ruta',
            name='fecha_hora_importacion',
            field=models.CharField(null=True, max_length=14, blank=True),
        ),
    ]
