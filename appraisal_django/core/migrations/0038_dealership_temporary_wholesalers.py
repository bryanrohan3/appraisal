# Generated by Django 5.0.6 on 2024-07-26 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_remove_appraisal_vehicle_photos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealership',
            name='temporary_wholesalers',
            field=models.ManyToManyField(blank=True, related_name='temporary_wholesaler_dealerships', to='core.wholesalerprofile'),
        ),
    ]
