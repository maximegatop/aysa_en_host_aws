# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0003_auto_20210723_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='configaccion_cabe',
            name='filtros_clientes',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
    ]
