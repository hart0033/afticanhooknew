# Generated by Django 4.2.3 on 2024-02-01 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijahook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='postads',
            name='services',
            field=models.ManyToManyField(to='naijahook.service'),
        ),
    ]
