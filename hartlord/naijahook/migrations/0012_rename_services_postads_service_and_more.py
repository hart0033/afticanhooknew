# Generated by Django 4.2.3 on 2024-02-05 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0011_rename_service_postads_services_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postads',
            old_name='services',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='services',
            new_name='service',
        ),
        migrations.AlterField(
            model_name='adsvideos',
            name='service',
            field=models.ManyToManyField(to='naijahook.service'),
        ),
    ]
