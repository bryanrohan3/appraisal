# Generated by Django 5.0.6 on 2024-07-26 03:47

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_alter_dealership_wholesalers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='temp_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.wholesalerprofile'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(default=core.models.default_wholesaler, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
