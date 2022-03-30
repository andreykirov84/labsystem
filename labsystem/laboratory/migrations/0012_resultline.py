# Generated by Django 4.0.3 on 2022-03-30 10:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0011_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(30)])),
                ('value', models.FloatField(blank=True, null=True, validators=[utils.validators.validate_value_not_negative])),
                ('comment', models.TextField(blank=True, null=True)),
                ('analysis_field_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.analysisfield')),
                ('result_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.result')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]