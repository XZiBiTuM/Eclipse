# Generated by Django 5.0.6 on 2024-09-24 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eclipse_app', '0013_alter_profile_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='changed',
            field=models.BooleanField(default=False, verbose_name='Подтверждены изменения'),
        ),
    ]
