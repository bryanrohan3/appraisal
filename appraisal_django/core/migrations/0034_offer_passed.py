# Generated by Django 5.0.6 on 2024-07-24 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_remove_offer_winner_appraisal_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]
