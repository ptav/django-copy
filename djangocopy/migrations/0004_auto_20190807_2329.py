# Generated by Django 2.0.10 on 2019-08-07 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocopy', '0003_auto_20190806_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='djangocopy/images')),
            ],
        ),
        migrations.AlterField(
            model_name='historicalnavbar',
            name='logo',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='A picture to use as a logo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='djangocopy.Image'),
        ),
        migrations.AlterField(
            model_name='navbar',
            name='logo',
            field=models.ForeignKey(blank=True, help_text='A picture to use as a logo', null=True, on_delete=django.db.models.deletion.SET_NULL, to='djangocopy.Image'),
        ),
        migrations.AlterField(
            model_name='template',
            name='template',
            field=models.FileField(upload_to='djangocopy/templates'),
        ),
    ]
