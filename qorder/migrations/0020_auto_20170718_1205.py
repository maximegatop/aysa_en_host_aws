# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0019_procesoimpexp_estado'),
    ]

    operations = [

        migrations.AddField(
            model_name='procesoimpexp',
            name='total',
            field=models.IntegerField(verbose_name='total', default=0),
        ),
    ]
