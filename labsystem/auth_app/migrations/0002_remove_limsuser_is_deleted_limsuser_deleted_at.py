# Generated by Django 4.0.3 on 2022-03-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='limsuser',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='limsuser',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
