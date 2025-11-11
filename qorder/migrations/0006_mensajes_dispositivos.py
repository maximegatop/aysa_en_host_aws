# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0005_auto_20220622_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensajes_Dispositivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('id_mensaje', models.CharField(max_length=150)),
                ('alias_dispositivo', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_hora_comando', models.DateTimeField(null=True, db_column='fecha_hora_comando', blank=True, verbose_name='fecha_hora_comando')),
                ('fecha_hora_respuesta', models.DateTimeField(null=True, db_column='fecha_hora_respuesta', blank=True, verbose_name='fecha_hora_respuesta')),
                ('tipo_mensaje', models.CharField(max_length=100, null=True, blank=True)),
                ('usuario_comando', models.CharField(max_length=100, null=True, blank=True)),
                ('comando_enviado', models.CharField(max_length=250, null=True, blank=True)),
                ('respuesta', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Mensajes Dispositivos',
                'verbose_name': 'Mensaje Dispositivo',
            },
        ),
    ]
