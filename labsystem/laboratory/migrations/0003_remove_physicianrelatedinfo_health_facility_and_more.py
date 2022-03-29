# Generated by Django 4.0.3 on 2022-03-28 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0002_alter_pidtype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicianrelatedinfo',
            name='health_facility',
        ),
        migrations.RemoveField(
            model_name='physicianrelatedinfo',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='staffrelatedinfo',
            name='department',
        ),
        migrations.RemoveField(
            model_name='staffrelatedinfo',
            name='position',
        ),
        migrations.RemoveField(
            model_name='staffrelatedinfo',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='contact_info',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='patient_relation_info',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='physician_relation_info',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='staff_relation_info',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.city'),
        ),
        migrations.AddField(
            model_name='profile',
            name='clinical_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='laboratory.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='health_facility',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='laboratory.healthfacility'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='laboratory.position'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='specialty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.specialty'),
        ),
        migrations.AddField(
            model_name='profile',
            name='telephone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='ContactInfo',
        ),
        migrations.DeleteModel(
            name='PatientRelatedInfo',
        ),
        migrations.DeleteModel(
            name='PhysicianRelatedInfo',
        ),
        migrations.DeleteModel(
            name='StaffRelatedInfo',
        ),
    ]
