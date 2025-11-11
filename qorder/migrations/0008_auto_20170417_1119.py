# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0007_historicoconsumo_anio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicoconsumo',
            name='id',
        ),
        migrations.AddField(
            model_name='historicoconsumo',
            name='codigo',
            field=models.CharField(verbose_name='codigo', serialize=False, max_length=50, primary_key=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicoconsumo',
            name='valor_consumo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicoconsumo',
            name='consumo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Consumo'),
        ),
    ]
