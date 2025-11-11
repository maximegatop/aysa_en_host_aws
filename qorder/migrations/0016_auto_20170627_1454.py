# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qorder', '0015_puntodesuministro_grupo_lectura'),
    ]

    operations = [

    ]