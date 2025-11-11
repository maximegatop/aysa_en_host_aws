# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0002_auto_20170216_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntodesuministro',
            name='rutasum',
            field=models.ForeignKey(to='qorder.RutaSum', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
