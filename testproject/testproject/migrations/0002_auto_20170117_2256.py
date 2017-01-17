# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testproject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childonetomany',
            name='my_parent',
            field=models.ForeignKey(related_name='my_otm_children', to='testproject.Parent'),
        ),
    ]
