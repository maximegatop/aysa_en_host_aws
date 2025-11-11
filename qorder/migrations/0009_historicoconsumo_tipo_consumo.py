# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0008_auto_20170417_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoconsumo',
            name='tipo_consumo',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, null=True, to='qorder.Codigo'),
        ),
    ]
