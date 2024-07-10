# Generated by Django 5.0.6 on 2024-07-03 04:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_dealerprofile_dealerships'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dealership',
            name='sales_dealers',
            field=models.ManyToManyField(blank=True, related_name='sales_dealerships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dealership',
            name='wholesalers',
            field=models.ManyToManyField(blank=True, related_name='wholesaler_dealerships', to=settings.AUTH_USER_MODEL),
        ),
    ]