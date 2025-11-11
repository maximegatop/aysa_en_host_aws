# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigAccion_Cabe',
            fields=[
                ('codigo', models.CharField(serialize=False, max_length=50, primary_key=True, verbose_name='Código')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
                ('activo', models.SmallIntegerField(default=1)),
                ('fecha_vigencia', models.DateField(blank=True, null=True, verbose_name='Fecha vigencia')),
                ('ultima_modif', models.DateTimeField(blank=True, null=True, verbose_name='Fecha última modificación')),
                ('usuario_modif', models.CharField(blank=True, null=True, max_length=100, verbose_name='ejecutado por')),
            ],
            options={
                'verbose_name_plural': 'Configuración acciones cabecera',
                'verbose_name': 'Configuración acción cabecera',
            },
        ),
        migrations.CreateModel(
            name='ConfigAccion_Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('codigo_cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Cliente')),
                ('codigo_config_accion_cabe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.ConfigAccion_Cabe')),
            ],
            options={
                'verbose_name_plural': 'Configuración acciones cliente',
                'verbose_name': 'Configuración acciones cliente',
            },
        ),
        migrations.CreateModel(
            name='ConfigAccion_Deta',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('tipo_accion', models.CharField(max_length=50, verbose_name='Tipo acción')),
                ('orden_ejecucion', models.SmallIntegerField(default=0)),
                ('parametro_adicional', models.CharField(blank=True, null=True, max_length=100, verbose_name='Parametro adicional')),
                ('obligatorio', models.SmallIntegerField(default=1, verbose_name='Obligatorio')),
                ('codigo_accion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Codigo')),
                ('codigo_config_accion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.ConfigAccion_Cabe')),
            ],
            options={
                'verbose_name_plural': 'Configuración acciones detalle',
                'verbose_name': 'Configuración acciones detalle',
            },
        ),
        migrations.AlterUniqueTogether(
            name='configaccion_cliente',
            unique_together=set([('codigo_config_accion_cabe', 'codigo_cliente')]),
        ),
    ]
