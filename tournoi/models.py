# from nis import match
from django.db.models import Q
from django.db import models


class MatchType(models.TextChoices):
    FINAL = "FINAL"
    SEMIFINAL = "SEMIFINAL"
    POULE = "POULE"
    AMICAL = "AMICAL"


class MatchState(models.TextChoices):
    reported = "reporte"
    current = "en cours"
    cancel = "annulé"
    finish = "terminé"
    to_program = "a programmé"


class Edition(models.Model):
    STATUS = (('programmed', 'programmed'), ('active', 'active'))
    name = models.CharField(max_length=50, null=False)
    begin_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    status = models.CharField(max_length=15, choices=STATUS)

    def __str__(self):
        return self.name


class Poule(models.Model):
    """" """
    name = models.CharField(max_length=50)
    add_date = models.DateField(auto_now_add=True)
    edition = models.ForeignKey(Edition,
                                on_delete=models.CASCADE,
                                null=False,
                                related_name='poules')

    def __str__(self):
        return self.name + "(" + self.edition.name + ")"


class Team(models.Model):
    name = models.CharField(max_length=50, null=False)
    abreviation = models.CharField(max_length=50, null=False, default="team")
    add_date = models.DateField(auto_now_add=True)
    logo = models.ImageField(
        upload_to='team/logos/',
        default="default.png",
    )
    poule = models.ForeignKey(Poule,
                              models.DO_NOTHING,
                              null=True,
                              blank=True,
                              related_name='teams')
    victory = models.SmallIntegerField(default=0)
    points = models.SmallIntegerField(default=0)
    defeat = models.SmallIntegerField(default=0)
    null = models.SmallIntegerField(default=0)
    red_cart = models.SmallIntegerField(default=0)
    yellow_cart = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.abreviation

    def get_rang(self):
        """obtenir le classement de cette equipe dans sa poule"""

        return self.poule.teams.filter(points__gt=self.points).count() + 1

    def get_num_players(self):
        return self.players.count()

    def get_num_played_matchs(self):
        return TeamMatch.objects.filter(
            Q(team1__id=self.id) | Q(team2__id=self.id),
            match__state=MatchState.finish).count()

    def get_num_scored_goals(self):
        return Goal.objects.filter(player__team=self.id).count()


class Match(models.Model):
    """A match between two teams."""
    add_date = models.DateField(auto_now_add=True)
    date_to_play = models.DateTimeField(null=True)
    stade_name = models.CharField(max_length=200, default='Stade Mateco')
    state = models.CharField(choices=MatchState.choices,
                             default=MatchState.to_program,
                             max_length=50)
    match_type = models.CharField(choices=MatchType.choices,
                                  default=MatchType.POULE,
                                  max_length=50)
    goal_team1 = models.SmallIntegerField(default=0)
    goal_team2 = models.SmallIntegerField(default=0)
    edition = models.ForeignKey(Edition,
                                null=False,
                                on_delete=models.CASCADE,
                                related_name='matches')
    title = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return f'{self.title} {self.state} {self.date_to_play}'

    @property
    def score(self):
        pass

    @property
    def next_match(self):
        pass

    @property
    def winner(self):
        if self.goal_team1 > self.goal_team2:
            return self.team1
        elif self.goal_team1 < self.goal_team2:
            return self.team2
        else:
            return None


class TeamMatch(models.Model):
    team1 = models.ForeignKey(Team,
                              on_delete=models.CASCADE,
                              related_name='team1')
    team2 = models.ForeignKey(Team,
                              on_delete=models.CASCADE,
                              related_name='team2')
    edition = models.ForeignKey(Edition,
                                null=False,
                                on_delete=models.CASCADE,
                                related_name='team_matchs')
    match = models.ForeignKey(Match, null=False, on_delete=models.CASCADE)

    # @property
    def winner(self):
        if self.match.state == MatchState.finish:
            if self.match.goal_team1 > self.match.goal_team2:
                return self.team1
            elif self.match.goal_team1 < self.match.goal_team2:
                return self.team2
            else:
                return None


class Player(models.Model):
    """Player"""
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=True, blank=True)
    dossard = models.IntegerField(default=1)
    matricule = models.CharField(max_length=20,
                                 null=True,
                                 blank=True,
                                 default="00000")
    photo = models.ImageField(upload_to='players/photos',
                              null=True,
                              blank=True)
    add_date = models.DateField(auto_now_add=True)
    top_player = models.BooleanField(default=False)

    edition = models.ForeignKey(Edition,
                                null=False,
                                on_delete=models.CASCADE,
                                related_name='players')
    team = models.ForeignKey(Team,
                             null=False,
                             on_delete=models.CASCADE,
                             related_name='players')
    # provisoire
    nb_match = models.IntegerField(default=3)
    nb_pass = models.IntegerField(default=0)

    def __str__(self):
        return self.name + "(" + self.surname + ")(" + self.matricule + ")"

    @property
    def total_goals(self):
        """return number of scored goals"""
        return self.goals.all().count()
    


class GoalType(models.TextChoices):
    CSC = "CSC"
    SP = "SP"
    N = "N"


class Goal(models.Model):
    """Stores a goal scored in a match by a specific player."""
    player = models.ForeignKey(Player,
                               on_delete=models.DO_NOTHING,
                               related_name='goals')
    match = models.ForeignKey(Match,
                              on_delete=models.DO_NOTHING,
                              related_name='goals')
    goal_type = models.CharField(choices=GoalType.choices, max_length=50)

    def __str__(self):
        return ("Goal by {} during {}").format(self.player, self.match)
