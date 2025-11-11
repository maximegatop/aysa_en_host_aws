# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0007_desc_accion'),
    ]

    operations = [
        migrations.AddField(
            model_name='configaccion_cliente',
            name='codigo_punto_suministro',
            field=models.ForeignKey(to='qorder.PuntoDeSuministro', blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='configaccion_cliente',
            unique_together=set([('codigo_config_accion_cabe', 'codigo_cliente', 'codigo_punto_suministro')]),
        ),
    ]
