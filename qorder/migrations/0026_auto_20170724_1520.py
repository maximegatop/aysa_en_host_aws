# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0025_auto_20170724_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparato',
            name='estado_aparato',
            field=models.CharField(null=True, verbose_name='Activo', max_length=50, blank=True),
        ),
    ]
