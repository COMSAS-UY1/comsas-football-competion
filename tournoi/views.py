from django.shortcuts import render
from django.db.models import Count
from django.views import View
from tournoi.models import Edition, Player, Goal, GoalType, PouleTeam, Team, MatchState
from core.models import News
from django.views.generic import TemplateView


class IndexView(View):
    """ Class view for home page """
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        if current_edition:
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
            pouleA = current_edition.poules.filter(name='Poule A')
            pouleB = current_edition.poules.filter(name='Poule B')
            classement_A = PouleTeam.objects.filter(poule=pouleA).order_by(
                    "-points")
            classement_B = PouleTeam.objects.filter(poule=pouleB).order_by(
                    "-points")
            
            teams = Team.objects.all()

            next_match = current_edition.matches.filter(
                state=MatchState.to_program).order_by("date_to_play",
                                                      "id").first()

            match_not_play = current_edition.matches.exclude(
                state=MatchState.finish)
            played_match = current_edition.matches.filter(
                state=MatchState.finish).order_by("-date_to_play")
            all_match = current_edition.matches.all().order_by(
                "date_to_play", "id")

            news = News.objects.filter(edition__status='active')
            context = {
                "current_edition": current_edition,
                "pouleA": pouleA,
                "pouleB": pouleB,
                'classement_A':classement_A,
                'classement_B':classement_B,
                "goals": goals,
                "teams": teams,
                "matchs": all_match,
                "next_match": next_match,
                "not_played": match_not_play,
                "played_match": played_match,
                "last_match": played_match.first(),
                "news": news
            }
        else:
            context = {}
        return render(request, self.template_name, context)


class MatchView(View):
    template_name = 'tournoi/matches.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        next_macthes = current_edition.matches.exclude(
            state=MatchState.finish).order_by("date_to_play")

        played_matches = current_edition.matches.filter(
            state=MatchState.finish).order_by("-date_to_play")
        
        
        context = {
            "next_macthes": next_macthes,
            "played_matches": played_matches,
            "next_macth": next_macthes.first(),
            "last_macth": played_matches.first(),
        }
        return render(request, self.template_name, context)


class TeamView(TemplateView):
    template_name = "tournoi/players.html"
