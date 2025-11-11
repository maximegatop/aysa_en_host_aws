# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0004_puntodesuministro_secuencia_teorica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntodesuministro',
            name='secuencia_teorica',
            field=models.IntegerField(blank=True, null=True, default=0),
        ),
    ]
