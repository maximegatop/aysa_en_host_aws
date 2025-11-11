# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0013_auto_20170621_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reorganizar',
            name='oficina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.WorkUnit', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reorganizar',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
