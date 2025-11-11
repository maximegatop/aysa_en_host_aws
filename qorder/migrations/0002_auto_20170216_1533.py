# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntodesuministro',
            name='gps_latitud',
            field=models.CharField(blank=True, null=True, max_length=14, verbose_name='latitud'),
        ),
        migrations.AlterField(
            model_name='puntodesuministro',
            name='gps_longitud',
            field=models.CharField(blank=True, null=True, max_length=14, verbose_name='longitud'),
        ),
    ]
