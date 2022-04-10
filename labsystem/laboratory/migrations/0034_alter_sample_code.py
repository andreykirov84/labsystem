# Generated by Django 4.0.3 on 2022-04-10 08:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0033_alter_healthfacility_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='code',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
