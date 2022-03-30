# Generated by Django 4.0.3 on 2022-03-30 09:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0009_alter_analysis_analysis_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(30)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
