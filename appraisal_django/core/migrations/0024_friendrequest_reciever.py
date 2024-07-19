# Generated by Django 5.0.6 on 2024-07-18 00:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='reciever',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='core.wholesalerprofile'),
        ),
    ]
