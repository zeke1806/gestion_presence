# Generated by Django 3.0 on 2019-12-30 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0010_auto_20191219_0812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evenement',
            old_name='presences',
            new_name='etudiants',
        ),
    ]