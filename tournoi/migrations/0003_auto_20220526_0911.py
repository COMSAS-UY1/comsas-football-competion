# Generated by Django 3.2 on 2022-05-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoi', '0002_player_dossard'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='nb_match',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='player',
            name='nb_pass',
            field=models.IntegerField(default=0),
        ),
    ]
