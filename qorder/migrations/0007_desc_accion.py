# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
        ('qorder', '0006_mensajes_dispositivos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desc_Accion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('id_descarga', models.CharField(max_length=50)),
                ('fecha_hora_registro', models.DateTimeField()),
                ('punto_suministro', models.CharField(null=True, max_length=50, verbose_name='Punto Suministro', blank=True)),
                ('num_contrato', models.CharField(null=True, max_length=50, verbose_name='Num.Contrato', blank=True)),
                ('tipo_accion', models.CharField(max_length=50, verbose_name='Tipo acción')),
                ('parametro_adicional', models.CharField(null=True, max_length=100, verbose_name='Parametro adicional', blank=True)),
                ('paso_accion', models.CharField(null=True, max_length=5, verbose_name='paso acción', blank=True)),
                ('valor_binario_relevado', models.FileField(null=True, upload_to='', verbose_name='Multimedia relevado', blank=True)),
                ('valor_texto_relevado', models.CharField(null=True, max_length=500, verbose_name='texto relevado', blank=True)),
                ('codigo_accion', models.ForeignKey(to='qorder.Codigo', on_delete=django.db.models.deletion.PROTECT)),
                ('codigo_config_accion', models.ForeignKey(to='qorder.ConfigAccion_Cabe', on_delete=django.db.models.deletion.PROTECT)),
                ('oficina', models.ForeignKey(to='core.WorkUnit', on_delete=django.db.models.deletion.PROTECT)),
                ('orden_trabajo', models.ForeignKey(to='qorder.OrdenDeTrabajo', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Descarga acción',
                'verbose_name_plural': 'Descarga acciones',
            },
        ),
    ]
