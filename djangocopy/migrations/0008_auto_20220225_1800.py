# Generated by Django 2.2.27 on 2022-02-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0007_auto_20220219_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalcopy',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalpage',
            name='id',
            field=models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='page',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='template',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]