# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0024_auto_20170724_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='piso',
            field=models.CharField(null=True, blank=True, max_length=50, verbose_name='Piso'),
        ),
    ]
