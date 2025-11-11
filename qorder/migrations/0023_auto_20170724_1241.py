# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0022_semanasgu_semanasre_suministros_suministros_gu_suministros_res'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='Frecuencia',
        ),
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='grupo_lectura',
        ),
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='id_localidad',
        ),
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='rutasum2',
        ),
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='secuencia_anterior2',
        ),
        migrations.RemoveField(
            model_name='puntodesuministro',
            name='secuencia_teorica2',
        ),
    ]
