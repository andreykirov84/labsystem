# Generated by Django 4.0.3 on 2022-03-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0007_analysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='analysis_field',
            field=models.ManyToManyField(blank=True, null=True, to='laboratory.analysisfield'),
        ),
    ]