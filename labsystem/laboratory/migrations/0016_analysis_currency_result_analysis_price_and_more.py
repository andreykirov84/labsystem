# Generated by Django 4.0.3 on 2022-03-30 15:17

import django.core.validators
from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0015_alter_analysisfield_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='currency',
            field=models.CharField(default='EUR', max_length=3, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AddField(
            model_name='result',
            name='analysis_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[utils.validators.validate_value_not_negative]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='currency',
            field=models.CharField(default='EUR', max_length=3, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AddField(
            model_name='result',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[utils.validators.validate_value_not_negative]),
        ),
        migrations.AddField(
            model_name='result',
            name='payment_type',
            field=models.CharField(choices=[('PAYMENT_BY_CARD', 'PAYMENT_BY_CARD'), ('CASH_PAYMENT', 'CASH_PAYMENT'), ('PAYMENT_TYPE_NOT_SPECIFIED', 'PAYMENT_TYPE_NOT_SPECIFIED')], default='PAYMENT_TYPE_NOT_SPECIFIED', max_length=26),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='analysis',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[utils.validators.validate_value_not_negative]),
        ),
    ]