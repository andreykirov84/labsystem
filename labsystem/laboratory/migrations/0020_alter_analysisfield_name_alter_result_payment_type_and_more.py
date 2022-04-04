# Generated by Django 4.0.3 on 2022-03-31 13:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0019_rename_analysis_id_result_analysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisfield',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='result',
            name='payment_type',
            field=models.CharField(choices=[('payment by card', 'payment by card'), ('cash payment', 'cash payment'), ('Not specified', 'Not specified')], max_length=15),
        ),
        migrations.AlterField(
            model_name='resultline',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]