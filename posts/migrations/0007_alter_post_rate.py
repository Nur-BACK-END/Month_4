# Generated by Django 5.1.6 on 2025-02-21 13:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rate',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
