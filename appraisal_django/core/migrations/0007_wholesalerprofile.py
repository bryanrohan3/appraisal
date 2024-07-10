# Generated by Django 5.0.6 on 2024-07-04 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_dealership_sales_dealers_dealership_wholesalers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WholesalerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wholesaler_name', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=255)),
                ('suburb', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('NSW', 'New South Wales'), ('QLD', 'Queensland'), ('SA', 'South Australia'), ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia'), ('ACT', 'Australian Capital Territory'), ('NT', 'Northern Territory')], max_length=3)),
                ('postcode', models.CharField(max_length=4)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]