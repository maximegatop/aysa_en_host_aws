# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0023_auto_20170724_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntodesuministro',
            name='piso',
            field=models.CharField(verbose_name='Piso', blank=True, null=True, max_length=100),
        ),
    ]
