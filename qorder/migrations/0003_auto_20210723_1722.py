# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0002_auto_20210716_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configaccion_cliente',
            name='codigo_cliente',
            field=models.ForeignKey(to='qorder.Cliente'),
        ),
        migrations.AlterField(
            model_name='configaccion_cliente',
            name='codigo_config_accion_cabe',
            field=models.ForeignKey(to='qorder.ConfigAccion_Cabe'),
        ),
        migrations.AlterField(
            model_name='configaccion_deta',
            name='codigo_accion',
            field=models.ForeignKey(to='qorder.Codigo'),
        ),
        migrations.AlterField(
            model_name='configaccion_deta',
            name='codigo_config_accion',
            field=models.ForeignKey(to='qorder.ConfigAccion_Cabe'),
        ),
    ]
