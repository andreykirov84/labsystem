# Generated by Django 4.0.3 on 2022-04-01 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0023_rename_result_id_resultline_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultline',
            old_name='result',
            new_name='result_id',
        ),
    ]