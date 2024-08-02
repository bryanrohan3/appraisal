# Generated by Django 5.0.6 on 2024-08-02 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_remove_wholesalerprofile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_made_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='invited_wholesalers',
            field=models.ManyToManyField(blank=True, related_name='invited_appraisals', through='core.Offer', to='core.wholesalerprofile'),
        ),
        migrations.DeleteModel(
            name='AppraisalInvite',
        ),
    ]
