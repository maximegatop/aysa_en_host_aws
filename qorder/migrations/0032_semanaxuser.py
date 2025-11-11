# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qorder', '0031_reubicacion_suministro'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemanaXUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('semana', models.CharField(verbose_name='semana', max_length=14, blank=True, null=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SemanaXUser',
                'verbose_name_plural': 'SemanaXUser',
            },
        ),
    ]
