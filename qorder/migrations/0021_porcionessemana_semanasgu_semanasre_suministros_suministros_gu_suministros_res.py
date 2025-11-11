# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qorder', '0020_auto_20170718_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='porcionessemana',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('PORCION', models.CharField(blank=True, max_length=100, null=True, verbose_name='PORCION')),
                ('SEMANA', models.CharField(blank=True, max_length=100, null=True, verbose_name='SEMANA')),
                ('REGION', models.CharField(blank=True, max_length=100, null=True, verbose_name='REGION')),
                ('DISTRITO', models.CharField(blank=True, max_length=100, null=True, verbose_name='DISTRITO')),
                ('DESCDISTRITO', models.CharField(blank=True, max_length=100, null=True, verbose_name='DESCDISTRITO')),
            ],
            options={
                'verbose_name': 'porcionessemana',
                'verbose_name_plural': 'porcionessemanas',
            },
        ),
        
    ]
