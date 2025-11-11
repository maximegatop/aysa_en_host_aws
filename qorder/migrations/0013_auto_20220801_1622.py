# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0012_auto_20220728_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resguardo_terreno',
            name='fecha_carga',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
