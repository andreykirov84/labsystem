# Generated by Django 4.0.3 on 2022-03-30 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0013_analysisfield_units_alter_analysis_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysisfield',
            old_name='units',
            new_name='unit',
        ),
    ]
