# Generated by Django 3.0 on 2019-12-19 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0007_tempimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempimage',
            name='name',
            field=models.CharField(default='temp', max_length=255),
            preserve_default=False,
        ),
    ]
