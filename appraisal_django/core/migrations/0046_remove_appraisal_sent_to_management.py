# Generated by Django 5.0.6 on 2024-07-30 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_remove_photo_damage_damage_image_alter_photo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='sent_to_management',
        ),
    ]