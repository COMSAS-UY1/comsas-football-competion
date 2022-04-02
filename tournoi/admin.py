from django.contrib import admin
from tournoi.models import Edition, Player, Poule, Match, PouleTeam, Team, Goal


class EditionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "begin_date", "end_date", "status"]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "surname", "add_date"]


class PouleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "edition", "add_date"]
    search_fields = ["id", "name"]


class PouleTeamAdmin(admin.ModelAdmin):
    list_display = [
        "id", "team", "poule", "points", "victory", "defeat",
        "null"
    ]
    search_fields = ["team", "poule", "victotry"]
    list_filter = ["team", "poule"]


class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abreviation", "add_date", "logo"]
    list_filter = ["abreviation"]
    search_fields = ["name"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id", "team1", "team2", "date_to_play", "goal_team1", "goal_team2",
        "edition"
    ]


class GoalAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "match", "goal_type"]


admin.site.register(Team, TeamAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(Poule, PouleAdmin)
admin.site.register(PouleTeam, PouleTeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)