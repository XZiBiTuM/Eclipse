# Generated by Django 5.0.6 on 2024-09-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eclipse_app', '0026_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
