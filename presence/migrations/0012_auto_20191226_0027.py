# Generated by Django 3.0 on 2019-12-26 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0011_evenement_groupe_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='presence.Categorie'),
        ),
    ]