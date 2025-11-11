# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0027_historicoconsumo_cod_anomalia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suministros',
            name='ACUM_CONS_VARIOS_RECAMBIOS',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO_ESTIMADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='CONSUMO_ULTIMO_RECAMBIO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA_ACTUAL',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA_ACTUAL_AUDIT',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA_ANTERIOR',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA_MAXIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LECTURA_MINIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='LEC_MEDIDOR_RETIRADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros',
            name='NRO_PUERTA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='ACUM_CONS_VARIOS_RECAMBIOS',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO_ESTIMADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='CONSUMO_ULTIMO_RECAMBIO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA_ACTUAL',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA_ACTUAL_AUDIT',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA_ANTERIOR',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA_MAXIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LECTURA_MINIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='LEC_MEDIDOR_RETIRADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_gu',
            name='NRO_PUERTA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='ACUM_CONS_VARIOS_RECAMBIOS',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO_ESTIMADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='CONSUMO_ULTIMO_RECAMBIO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA1',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA2',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA3',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA4',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA5',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA6',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA_ACTUAL',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA_ACTUAL_AUDIT',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA_ANTERIOR',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA_MAXIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LECTURA_MINIMA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='LEC_MEDIDOR_RETIRADO',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
        migrations.AlterField(
            model_name='suministros_res',
            name='NRO_PUERTA',
            field=models.DecimalField(decimal_places=7, max_digits=8),
        ),
    ]
