# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
        ('qorder', '0009_auto_20220718_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtensionDatos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('tabla_extension', models.CharField(verbose_name='Tabla extensión', max_length=50)),
                ('campo_extension', models.CharField(verbose_name='Campo extensión', max_length=50)),
                ('clave_registro', models.CharField(verbose_name='Clave registro', max_length=50, db_index=True)),
                ('valor', models.CharField(verbose_name='Valor', max_length=500, blank=True, null=True)),
                ('etiqueta_campo_extension', models.CharField(verbose_name='Etiqueta campo extensión', max_length=50, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'extension_dato',
                'verbose_name_plural': 'extension_datos',
            },
        ),
        migrations.CreateModel(
            name='Resguardo_Terreno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_generacion', models.DateField(blank=True, null=True)),
                ('cuenta_contrato', models.CharField(max_length=30, blank=True, null=True)),
                ('nombre_apellido', models.CharField(max_length=250, blank=True, null=True)),
                ('numero_ruta', models.CharField(max_length=8, blank=True, null=True)),
                ('itinerario', models.CharField(max_length=8, blank=True, null=True)),
                ('ciclo', models.CharField(max_length=8, blank=True, null=True)),
                ('tipo_orden', models.CharField(max_length=4, blank=True, null=True)),
                ('clase_actividad', models.CharField(max_length=4, blank=True, null=True)),
                ('fh_inicio', models.DateField(blank=True, null=True)),
                ('fh_fin', models.DateField(blank=True, null=True)),
                ('lectura', models.IntegerField(blank=True, null=True)),
                ('lectura_anterior', models.IntegerField(blank=True, null=True)),
                ('consumo', models.IntegerField(blank=True, null=True)),
                ('cargado', models.NullBooleanField()),
                ('descargado', models.NullBooleanField()),
                ('fecha_descarga', models.DateField(blank=True, null=True)),
                ('fecha_asignacion', models.DateField(blank=True, null=True)),
                ('fecha_carga', models.DateField(blank=True, null=True)),
                ('estado', models.BigIntegerField(blank=True, null=True)),
                ('alias_dispositivo', models.CharField(max_length=20, blank=True, null=True)),
                ('tiene_auditoria', models.NullBooleanField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Cliente')),
                ('cod_ruta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Ruta')),
                ('oficina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.WorkUnit')),
                ('orden_trabajo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.OrdenDeTrabajo')),
                ('punto_suministro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.PuntoDeSuministro')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qorder.Tecnico')),
                ('usuario_asignacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'resguardo_terreno',
                'verbose_name_plural': 'resguardos_terreno',
            },
        ),
        migrations.AlterIndexTogether(
            name='extensiondatos',
            index_together=set([('tabla_extension', 'campo_extension', 'clave_registro')]),
        ),
    ]
