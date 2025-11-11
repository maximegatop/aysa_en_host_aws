# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0010_auto_20170608_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodesuministro',
            name='id_localidad',
            field=models.CharField(max_length=10, verbose_name='id_localidad', null=True, blank=True),
        ),
    ]
