# Generated by Django 2.2.11 on 2020-06-11 08:03

import character.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0005_auto_20200611_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='transform_o',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_transform),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_x',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_transform),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_y',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_transform),
        ),
        migrations.AlterField(
            model_name='character',
            name='transform_z',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=character.models.get_default_transform),
        ),
        migrations.AlterUniqueTogether(
            name='character',
            unique_together={('first_name', 'last_name')},
        ),
    ]
