# Generated by Django 4.0.3 on 2022-04-08 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('begin_date', models.DateField(default=None, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
                ('status', models.CharField(choices=[('programmed', 'programmed'), ('active', 'active')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True)),
                ('date_to_play', models.DateTimeField(null=True)),
                ('stade_name', models.CharField(default='Stade Mateco', max_length=200)),
                ('state', models.CharField(choices=[('reporte', 'Reported'), ('en cours', 'Current'), ('annulé', 'Cancel'), ('terminé', 'Finish'), ('a programmé', 'To Program')], default='a programmé', max_length=50)),
                ('match_type', models.CharField(choices=[('FINAL', 'Final'), ('SEMIFINAL', 'Semifinal'), ('POULE', 'Poule'), ('AMICAL', 'Amical')], default='POULE', max_length=50)),
                ('goal_team1', models.SmallIntegerField(default=0)),
                ('goal_team2', models.SmallIntegerField(default=0)),
                ('title', models.CharField(default=None, max_length=50, null=True)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='tournoi.edition')),
            ],
        ),
        migrations.CreateModel(
            name='Poule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poules', to='tournoi.edition')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abreviation', models.CharField(default='team', max_length=50)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('logo', models.ImageField(default='default.png', upload_to='team/logos/')),
                ('victory', models.SmallIntegerField(default=0)),
                ('points', models.SmallIntegerField(default=0)),
                ('defeat', models.SmallIntegerField(default=0)),
                ('null', models.SmallIntegerField(default=0)),
                ('red_cart', models.SmallIntegerField(default=0)),
                ('yellow_cart', models.SmallIntegerField(default=0)),
                ('poule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='teams', to='tournoi.poule')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_matchs', to='tournoi.edition')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournoi.match')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='tournoi.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='tournoi.team')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(blank=True, max_length=50, null=True)),
                ('matricule', models.CharField(blank=True, default='00000', max_length=20, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='players/photos')),
                ('add_date', models.DateField(auto_now_add=True)),
                ('top_player', models.BooleanField(default=False)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournoi.edition')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournoi.team')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.CharField(choices=[('CSC', 'Csc'), ('SP', 'Sp'), ('N', 'N')], max_length=50)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='goals', to='tournoi.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='goals', to='tournoi.player')),
            ],
        ),
    ]
