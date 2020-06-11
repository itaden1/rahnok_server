# Generated by Django 2.2.11 on 2020-06-11 06:12

import character.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0004_auto_20200611_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='appearance',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_appearance),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_o',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_appearance),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_x',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_appearance),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_y',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_appearance),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_z',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_appearance),
        ),
    ]