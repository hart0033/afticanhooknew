# Generated by Django 4.2.3 on 2024-06-28 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0027_remove_adsvideos_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsvideos',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]
