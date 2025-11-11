# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0004_configaccion_cabe_filtros_clientes'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminalportatil',
            name='token',
            field=models.CharField(verbose_name='token', blank=True, null=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='configaccion_cabe',
            name='filtros_clientes',
            field=models.CharField(blank=True, null=True, max_length=512),
        ),
    ]
