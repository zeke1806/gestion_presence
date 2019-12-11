# Generated by Django 3.0 on 2019-12-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presence', '0004_evenement_responsables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='date_debut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date_fin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='presences',
            field=models.ManyToManyField(blank=True, null=True, related_name='evenements', to='presence.Etudiant'),
        ),
    ]
