# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
        ('qorder', '0030_auto_20180103_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='reubicacion_suministro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ruta', models.CharField(null=True, max_length=100, verbose_name='ruta', blank=True)),
                ('itinerario', models.CharField(null=True, max_length=100, verbose_name='itinerario', blank=True)),
                ('punto_suministro', models.CharField(null=True, max_length=100, verbose_name='punto_suministro', blank=True)),
                ('secuencia_teorica', models.IntegerField(null=True, verbose_name='secuencia_teorica', blank=True)),
                ('direccion', models.CharField(null=True, max_length=100, verbose_name='direccion', blank=True)),
                ('numero_puerta', models.DecimalField(decimal_places=7, max_digits=8)),
                ('porcion_original', models.CharField(null=True, max_length=100, verbose_name='porcion_original', blank=True)),
                ('sec_original', models.IntegerField(null=True, verbose_name='sec_original', blank=True)),
                ('unidad_original', models.CharField(null=True, max_length=100, verbose_name='unidad_original', blank=True)),
                ('oficina', models.ForeignKey(null=True, to='core.WorkUnit', blank=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'reubicacion_suministro',
                'verbose_name_plural': 'reubicacion_suministros',
            },
        ),
    ]
