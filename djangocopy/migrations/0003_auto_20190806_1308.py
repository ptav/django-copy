# Generated by Django 2.0.10 on 2019-08-06 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0002_historicalcopy_historicalnavbar_historicalpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnavbar',
            name='label',
            field=models.CharField(default='Blank', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='navbar',
            name='label',
            field=models.CharField(default='Blank', max_length=255),
            preserve_default=False,
        ),
    ]