# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qorder', '0011_puntodesuministro_id_localidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reorganizar',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(null=True, blank=True)),
                ('fecha_autorizado', models.DateTimeField(null=True, blank=True)),
                ('fecha_denegado', models.DateTimeField(null=True, blank=True)),
                ('Oficina', models.ForeignKey(to='core.WorkUnit', on_delete=django.db.models.deletion.PROTECT)),
                ('Usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
                ('ruta', models.ForeignKey(to='qorder.Ruta', on_delete=django.db.models.deletion.PROTECT)),
                ('tecnico_solicito', models.ForeignKey(to='qorder.Tecnico', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'Reorganizar',
                'verbose_name': 'Reorganizar',
            },
        ),
        migrations.AddField(
            model_name='puntodesuministro',
            name='fecha_actualizacion_secuencia',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='puntodesuministro',
            name='secuencia_anterior',
            field=models.IntegerField(null=True, default=0, blank=True),
        ),
        migrations.AddField(
            model_name='puntodesuministro',
            name='secuencia_anterior2',
            field=models.IntegerField(null=True, default=0, blank=True),
        ),
    ]
