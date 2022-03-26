from email.mime import image
from pyexpat import model
from turtle import title
from django.db import models


class Edition(models.Model):
    name = models.CharField(max_length=50, null=False)
    begin_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    programmed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50, null=False)
    abreviation = models.CharField(max_length=50, null=False, default="team")
    add_date = models.DateField(auto_now_add=True)
    logo = models.ImageField(upload_to='team/logos/', default="default.png",)
    
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
    date_to_play = models.DateField(null=True)
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
    winner = models.SmallIntegerField(default=0)
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


class Player(models.Model):
    """Player"""
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=True, blank=True)
    matricule = models.CharField(max_length=20,
                                 null=True,
                                 blank=True,
                                 default="00000")
    photo = models.ImageField(upload_to='players/photos', null=True, blank=True)
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + "(" + self.surname + ")(" + self.matricule + ")"

    @property
    def total_goals(self):
        """return number of scored goals"""
        return self.goals.all().count()


class Goal(models.Model):
    """Stores a goal scored in a match by a specific player."""
    player = models.ForeignKey(Player,
                               on_delete=models.DO_NOTHING,
                               related_name='goals')
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    goal_type = models.CharField(choices=GoalType.choices, max_length=50)

    def __str__(self):
        return _("Goal by {} during {}").format(self.player, self.match)


class Poule(models.Model):
    """" """
    name = models.CharField(max_length=50)
    add_date = models.DateField(auto_now_add=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=False, related_name='poules')

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

class ContactInfo(models.Model):
    '''Manages the contact form/page'''
    name = models.CharField(max_length = 150, null=False, blank=False, error_messages={'required': ("Veuillez entrer votre nom et prénom.")})
    email = models.EmailField(null=True, blank=True, error_messages={'required': ("Veuillez entrer votre adresse email.")})
    phone = models.CharField(max_length=9, null=False, blank=False, error_messages={'required': ("Veuillez entrer votre numéro de téléphone.")})
    subject = models.CharField(max_length = 100, error_messages={'required': ("Veuillez entrer le titre de votre message.")})
    message = models.TextField(null=False, blank=False, error_messages={'required': ("Veuillez entrer votre message.")})

    def __str__(self):
        return self.name + ' ' + self.subject

class News(models.Model):
    image = models.ImageField(upload_to='actualite/', default="news_placeholder.jpg",)
    title = models.CharField(max_length = 50, null=False, blank=False,)
    description = models.CharField(max_length = 150, null=False, blank=False,)
    
    def __str__(self):
        return self.title

class GalleryFilter(models.Model):
    pass
    '''
        Le model ci est lie au suivant. Ca sera en fonction d'un filtre qu'on affichera les images.
        Il y aura au tout d'abord un premier filtre qui montrera toutes les images prises.
        Les autres viendront apres un evenement (donc sera creer dans le admin dashboard). 
        Voir gallery.html
        Donc comme filtres on peut avoir Tous (au debut). Apres la premiere journee de matchs, 
        on cree un nouveau filtre "match 1" ou "match + date" qui contiendra uniquement les images 
        de cette journee.
    '''
    

class Gallery(models.Model):
    image =  models.ImageField(upload_to='gallerie/', null=False)
    alt = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)

    