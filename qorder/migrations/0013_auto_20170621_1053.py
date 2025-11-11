# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0012_auto_20170619_1316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reorganizar',
            old_name='Oficina',
            new_name='oficina',
        ),
        migrations.RenameField(
            model_name='reorganizar',
            old_name='Usuario',
            new_name='usuario',
        ),
    ]
