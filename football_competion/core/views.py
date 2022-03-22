from django.shortcuts import render
from django.views import View


class IndexView(View):
    """ Class view for home page """
    template_name = 'core/index.htmŀ'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(active=True).first()
        # get all scorers in the current edition
        top_scorers = Player.goals.filter(
            match__edition=current_edition.id).annotate(
                num_goals=Count('goals')).order_by("-num_goals")
        # get stats
        poules = current_edition.poules.all()
        classement = {}
        for poule in poules:
            poule_teams = PouleTeam.objects.filter(poule=poule).order_by(
                "-points", "-goals_average")
            classements[poule.name] = classement

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
            "active_edition": active_edition,
            "poules": poules,
            "standing": classements,
            "players": players,
            "teams": teams,
            "matchs": all_match,
            "next_match": next_match,
            "not_played": match_not_play,
            "played": played_match,
            "goals": goals
        }
        return render(request, self.template_name, context)


class MatchView(View):
    template_name = 'core/match.html'

    def get(self, request, *args, **kwargs):
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
