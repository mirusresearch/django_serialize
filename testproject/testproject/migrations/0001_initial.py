# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChildManyToMany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('another_char_property', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChildOneToMany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChildOneToOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('some_int_property', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('some_char_property', models.CharField(max_length=50, null=True, blank=True)),
                ('a_many_to_many_child', models.ManyToManyField(to='testproject.ChildManyToMany')),
                ('a_one_to_one_child', models.OneToOneField(null=True, blank=True, to='testproject.ChildOneToOne')),
            ],
        ),
        migrations.AddField(
            model_name='childonetomany',
            name='my_parent',
            field=models.ForeignKey(to='testproject.Parent'),
        ),
    ]
