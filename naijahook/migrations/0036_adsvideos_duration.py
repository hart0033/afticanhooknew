# Generated by Django 4.2.3 on 2024-08-29 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0035_alter_postads_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsvideos',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
