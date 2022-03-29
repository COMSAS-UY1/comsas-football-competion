from django.db import models


class Edition(models.Model):
    STATUS = (('programmed', 'programmed'), ('active', 'active'))
    name = models.CharField(max_length=50, null=False)
    begin_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    status = models.CharField(max_length=15, choices=STATUS)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50, null=False)
    abreviation = models.CharField(max_length=50, null=False, default="team")
    add_date = models.DateField(auto_now_add=True)
    logo = models.ImageField(
        upload_to='team/logos/',
        default="default.png",
    )

    def __str__(self):
        return self.abreviation


class GoalType(models.TextChoices):
    CSC = "CSC"
    SP = "SP"
    N = "N"


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


class Match(models.Model):
    """A match between two teams."""
    add_date = models.DateField(auto_now_add=True)
    date_to_play = models.DateTimeField(null=True)
    state = models.CharField(choices=MatchState.choices,
                             default=MatchState.to_program,
                             max_length=50)
    match_type = models.CharField(choices=MatchType.choices,
                                  default=MatchType.POULE,
                                  max_length=50)
    team1 = models.ForeignKey(Team,
                              on_delete=models.CASCADE,
                              related_name="team1")
    team2 = models.ForeignKey(Team,
                              on_delete=models.CASCADE,
                              related_name="team2")
    goal_team1 = models.SmallIntegerField(default=0)
    goal_team2 = models.SmallIntegerField(default=0)
    #penalty = models.BooleanField(default=False, )  #vrai si les equipes sont allés au penalty
    edition = models.ForeignKey(Edition,
                                null=False,
                                on_delete=models.CASCADE,
                                related_name='matches')
    title = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return self.team1.name + " vs " + self.team2.name + "(" + self.edition.name + ")" + "(" + self.state + ")"

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


class Player(models.Model):
    """Player"""
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=True, blank=True)
    matricule = models.CharField(max_length=20,
                                 null=True,
                                 blank=True,
                                 default="00000")
    photo = models.ImageField(upload_to='players/photos',
                              null=True,
                              blank=True)
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + "(" + self.surname + ")(" + self.matricule + ")"

    @property
    def total_goals(self):
        """return number of scored goals"""
        return self.goals.all().count()


# class PLayerTeam(models.Model):
#     edition = models.ForeignKey(Edition, models.CASCADE)
#     team = models.ForeignKey(Team, models.CASCADE)
#     player = models.ForeignKey(Player, models.CASCADE)


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


class PouleTeam(models.Model):
    """ Stocke chaque ligne dans le tableau de statisque"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False)
    poule = models.ForeignKey(Poule, on_delete=models.CASCADE, null=False)
    goals = models.SmallIntegerField(default=0)
    points = models.SmallIntegerField(default=0)
    conceded_goals = models.SmallIntegerField(default=0)
    goals_average = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.team.name + " " + self.poule.__str__()