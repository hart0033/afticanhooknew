# Generated by Django 4.2.3 on 2024-02-05 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0009_remove_adsvideos_services_remove_postads_services_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postads',
            name='service',
            field=models.ManyToManyField(to='naijahook.service'),
        ),
    ]
