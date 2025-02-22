# Generated by Django 2.1.1 on 2018-10-13 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangocopy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCopy',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('url', models.CharField(blank=True, help_text='URL name (leave empty to load for all templates)', max_length=255)),
                ('fieldid', models.SlugField(help_text='The field identifier that will be used in templates', max_length=100)),
                ('locale', models.CharField(blank=True, help_text="Browser settings (e.g. 'en_GB')", max_length=5)),
                ('geo', models.CharField(blank=True, help_text="Country code derived from the IP (e.g. 'GB')", max_length=2)),
                ('text', models.TextField(max_length=10000)),
                ('format', models.CharField(choices=[('p', 'Plain text'), ('m', 'Markdown'), ('j', 'JSON'), ('h', 'HTML'), ('s', 'Special HTML')], default='p', max_length=1)),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], default='d', max_length=1)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical copy',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalNavbar',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('logo', models.TextField(blank=True, help_text='A picture to use as a logo', max_length=100, null=True)),
                ('elements', models.JSONField()),
                ('z_index', models.IntegerField(default=0, help_text='The z-index determines the order of navbar items. A higher value appears first.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical navbar',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPage',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('authenticated', models.BooleanField(default=False, help_text='If True, visitor must login to access this page')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('keywords', models.CharField(blank=True, default='', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('template', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='djangocopy.Template')),
            ],
            options={
                'verbose_name': 'historical page',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
