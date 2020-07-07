# Generated by Django 2.1.1 on 2018-10-12 06:56

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, help_text='URL name (leave empty to load for all templates)', max_length=255)),
                ('fieldid', models.SlugField(help_text='The field identifier that will be used in templates', max_length=100)),
                ('locale', models.CharField(blank=True, help_text="Browser settings (e.g. 'en_GB')", max_length=5)),
                ('geo', models.CharField(blank=True, help_text="Country code derived from the IP (e.g. 'GB')", max_length=2)),
                ('text', models.TextField(max_length=10000)),
                ('format', models.CharField(choices=[('p', 'Plain text'), ('m', 'Markdown'), ('j', 'JSON'), ('h', 'HTML'), ('s', 'Special HTML')], default='p', max_length=1)),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], default='d', max_length=1)),
            ],
            options={
                'verbose_name_plural': 'copy',
            },
        ),
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, help_text='A picture to use as a logo', null=True, upload_to='djangocopy/')),
                ('elements', jsonfield.fields.JSONField()),
                ('z_index', models.IntegerField(default=0, help_text='The z-index determines the order of navbar items. A higher value appears first.')),
                ('groups', models.ManyToManyField(blank=True, help_text='Associate navbar with a particular user group.', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('authenticated', models.BooleanField(default=False, help_text='If True, visitor must login to access this page')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('keywords', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('template', models.FileField(upload_to='templates')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='djangocopy.Template'),
        ),
        migrations.AlterUniqueTogether(
            name='copy',
            unique_together={('fieldid', 'url', 'locale', 'geo', 'status')},
        ),
    ]