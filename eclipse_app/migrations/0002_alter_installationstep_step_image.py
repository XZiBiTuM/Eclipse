# Generated by Django 5.0.6 on 2024-09-12 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eclipse_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installationstep',
            name='step_image',
            field=models.ImageField(blank=True, upload_to='installation_steps/', verbose_name='Изображение шага'),
        ),
    ]
