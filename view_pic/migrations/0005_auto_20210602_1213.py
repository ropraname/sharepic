# Generated by Django 3.1.3 on 2021-06-02 09:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_pic', '0004_auto_20210531_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grading',
            name='rate_content_meaning',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='grading',
            name='rate_draw_technique',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='grading',
            name='rate_originality',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
