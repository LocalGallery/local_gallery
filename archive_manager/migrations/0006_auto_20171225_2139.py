# Generated by Django 2.0 on 2017-12-25 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_manager', '0005_auto_20171225_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='name',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
