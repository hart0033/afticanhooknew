# Generated by Django 4.2.3 on 2024-02-02 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0006_customuser_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='escort',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
