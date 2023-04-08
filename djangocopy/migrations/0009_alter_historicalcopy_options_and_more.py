# Generated by Django 4.2 on 2023-04-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0008_auto_20220225_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalcopy',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical copy', 'verbose_name_plural': 'historical copy'},
        ),
        migrations.AlterModelOptions(
            name='historicalnavbar',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical navbar', 'verbose_name_plural': 'historical navbars'},
        ),
        migrations.AlterModelOptions(
            name='historicalpage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical page', 'verbose_name_plural': 'historical pages'},
        ),
        migrations.AlterField(
            model_name='copy',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalcopy',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalcopy',
            name='id',
            field=models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='elements',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='id',
            field=models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalpage',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalpage',
            name='id',
            field=models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='elements',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='page',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='template',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
