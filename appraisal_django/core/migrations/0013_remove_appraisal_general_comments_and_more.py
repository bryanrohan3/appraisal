# Generated by Django 5.0.6 on 2024-07-09 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_appraisal_sent_to_management'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='general_comments',
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='privacy_comments',
        ),
    ]
