# Generated by Django 4.2 on 2023-05-06 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0001_squashed_0009_alter_historicalcopy_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnavbar',
            name='anonymous',
            field=models.BooleanField(default=False, help_text='If True, navbar is shown to anonymous users. If False (default), navbar is shown to authenticated users only.'),
        ),
        migrations.AddField(
            model_name='navbar',
            name='anonymous',
            field=models.BooleanField(default=False, help_text='If True, navbar is shown to anonymous users. If False (default), navbar is shown to authenticated users only.'),
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='label',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='label',
            field=models.CharField(max_length=255),
        ),
    ]