# Generated by Django 3.0 on 2019-12-19 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0006_auto_20191211_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='temp/')),
            ],
        ),
    ]