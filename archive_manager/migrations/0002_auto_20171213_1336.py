# Generated by Django 2.0 on 2017-12-13 11:36

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='photo desc', max_length=100)),
                ('photo_file', models.ImageField(upload_to='photos/local_photos', verbose_name='Local Photo')),
                ('date_taken', models.DateField()),
                ('date_added', models.DateField(blank=True, null=True)),
                ('tags_array', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None)),
            ],
        ),
        migrations.AlterField(
            model_name='location',
            name='information',
            field=models.TextField(default='localtion info', max_length=15),
        ),
        migrations.AddField(
            model_name='photo',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive_manager.Location'),
        ),
    ]
