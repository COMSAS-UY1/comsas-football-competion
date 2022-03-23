from nis import match
from django.shortcuts import render
from django.db.models import Count
from django.views import View
from core.models import Edition, Player, Goal, GoalType, PouleTeam, Team, MatchState


class IndexView(View):
    """ Class view for home page """
    template_name = 'core/index.htmŀ'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(active=True).first()
        if current_edition:
            # get all scorers in the current edition
            goals = Goal.objects.exclude(
                goal_type=GoalType.CSC,
                match__edition__active=False).values("player").annotate(
                    nbgoal=Count("id"),
                    nbmatch=Count("match")).order_by("-nbgoal", "match")
            for i, elt in enumerate(goals):
                goals[i]["player"] = Player.objects.filter(
                    id=goals[i]["player"]).first()
            # get stats
            poules = current_edition.poules.all()
            classements = {}
            for poule in poules:
                poule_teams = PouleTeam.objects.filter(poule=poule).order_by(
                    "-points", "-goals_average")
                classements[poule.name] = poule_teams

            teams = Team.objects.all()

            next_match = current_edition.matches.filter(
                state=MatchState.to_program).order_by("date_to_play",
                                                      "id").first()

            match_not_play = current_edition.matches.exclude(
                state=MatchState.finish)
            played_match = current_edition.matches.filter(
                state=MatchState.finish).order_by("-date_to_play", "-id")
            all_match = current_edition.matches.all().order_by(
                "date_to_play", "id")

            context = {
                "current_edition": current_edition,
                "poules": poules,
                "standing": classements,
                "goals": goals,
                "teams": teams,
                "matchs": all_match,
                "next_match": next_match,
                "not_played": match_not_play,
                "played": played_match,
            }
        else:
            context = {}
        return render(request, self.template_name, context)


class MatchView(View):
    template_name = 'core/match.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(active=True).first()
        match_not_play = current_edition.matches.exclude(
            state=MatchState.finish).order_by("date_to_play")

        played_match = current_edition.matches.filter(
            state=MatchState.finish).order_by("-date_to_play")
        all_match = current_edition.matches.all().order_by("date_to_play")
        context = {
            "to_plays": match_not_play,
            "played_matchs": played_match,
            "all_match": match_not_play
        }
        return render(request, "core/match.html", context)
