# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0003_auto_20170327_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodesuministro',
            name='secuencia_teorica',
            field=models.IntegerField(default=0),
        ),
    ]
