# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0014_auto_20170621_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodesuministro',
            name='grupo_lectura',
            field=models.CharField(max_length='2', verbose_name='grupo_lectura', blank=True, null=True),
        ),
    ]
