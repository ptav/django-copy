# Generated by Django 2.0.10 on 2019-08-07 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0004_auto_20190807_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='label',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='template',
            name='label',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]