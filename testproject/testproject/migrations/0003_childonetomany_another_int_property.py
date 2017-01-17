# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testproject', '0002_auto_20170117_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='childonetomany',
            name='another_int_property',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
