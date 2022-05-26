from pprint import pprint
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django.views import View
from tournoi.models import Edition, Player, Goal, GoalType, Team, MatchState, TeamMatch
from core.models import News


class IndexView(View):
    """ Class view for home page """
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = get_object_or_404(Edition, status='active')
        # get all scorers in the current edition
        goals = Goal.objects.exclude(
            goal_type=GoalType.CSC,
            match__edition__status='active').values("player").annotate(
                nbgoal=Count("id"),
                nbmatch=Count("match")).order_by("-nbgoal", "match")
        for i, elt in enumerate(goals):
            goals[i]["player"] = Player.objects.filter(
                id=goals[i]["player"]).first()

        # get stats
        pouleA = current_edition.poules.filter(name='Poule A').first()
        pouleB = current_edition.poules.filter(name='Poule B').first()
        classement_A = pouleA.teams.all().order_by("-points")
        classement_B = pouleB.teams.all().order_by("-points")

        next_match = TeamMatch.objects.filter(
            edition=current_edition,
            match__state=MatchState.to_program).order_by(
                'match__date_to_play').first()
        last_match = TeamMatch.objects.filter(
            edition=current_edition, match__state=MatchState.finish).order_by(
                '-match__date_to_play').first()

        news = News.objects.filter(edition__status='active')

        top_players = current_edition.players.filter(
            top_player=True).order_by("-add_date")

        context = {
            "current_edition": current_edition,
            "pouleA": pouleA,
            "pouleB": pouleB,
            'classement_A': classement_A,
            'classement_B': classement_B,
            "goals": goals,
            'last_match': last_match,
            "next_match": next_match,
            "top_players": top_players,
            'news': news
        }
        return render(request, self.template_name, context)


class MatchView(View):
    template_name = 'tournoi/matches.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        next_matchs = TeamMatch.objects.filter(
            edition=current_edition,
            match__state=MatchState.to_program).order_by('match__date_to_play')

        played_matches = TeamMatch.objects.filter(
            edition=current_edition,
            match__state=MatchState.finish).order_by('-match__date_to_play')

        # get stats
        pouleA = current_edition.poules.filter(name='Poule A').first()
        pouleB = current_edition.poules.filter(name='Poule B').first()
        classement_A = pouleA.teams.all().order_by("-points")
        classement_B = pouleB.teams.all().order_by("-points")
        top_players = current_edition.players.filter(
            top_player=True).order_by("dossard")

        context = {
            "current_edition": current_edition,
            "pouleA": pouleA,
            "pouleB": pouleB,
            'classement_A': classement_A,
            'classement_B': classement_B,
            "next_matchs": next_matchs,
            "played_matches": played_matches,
            "next_match": next_matchs.first(),
            "last_match": played_matches.first(),
            "last_matchs": played_matches,
            "top_players": top_players,
        }
        return render(request, self.template_name, context)


class TeamView(View):
    template_name = "tournoi/players.html"

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        teams = Team.objects.all()

        top_players = current_edition.players.filter(
            top_player=True).order_by("dossard")

        passeurs = current_edition.players.all().order_by('-nb_pass')[:5]
        # get all scorers in the current edition
        goals = Goal.objects.exclude(
            goal_type=GoalType.CSC,
            match__edition__status='active').values("player").annotate(
                nbgoal=Count("id"),
                nbmatch=Count("match")).order_by("-nbgoal", "match")
        for i, elt in enumerate(goals):

            goals[i]["player"] = Player.objects.filter(
                id=goals[i]["player"]).first()

        context = {
            "top_players": top_players,
            'teams': teams,
            'goals': goals,
            'passeurs': passeurs
        }
        return render(request, self.template_name, context)