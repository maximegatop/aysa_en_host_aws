# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qorder', '0008_auto_20220714_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoConfigAccion_Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateTimeField(null=True, blank=True)),
                ('codigo_cliente', models.ForeignKey(to='qorder.Cliente')),
                ('codigo_config_accion_cabe', models.ForeignKey(to='qorder.ConfigAccion_Cabe')),
                ('codigo_punto_suministro', models.ForeignKey(to='qorder.PuntoDeSuministro', blank=True, null=True)),
                ('usuario_asignacion', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Historico Configuración acciones cliente',
                'verbose_name': 'Historico Configuración acciones cliente',
            },
        ),
        migrations.AlterUniqueTogether(
            name='historicoconfigaccion_cliente',
            unique_together=set([('codigo_config_accion_cabe', 'codigo_cliente', 'codigo_punto_suministro', 'fecha')]),
        ),
    ]
